from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator




# Create your views here.
def index(request):
    context={
        "title":"Anasayfa",

    }
    return render(request, 'index.html',context)

def Register(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email").lower()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            charup = False
            charnum = False
            for char in password1:
                if char.isupper():
                    charup = True
                if char.isnumeric():
                    charnum = True
            if charnum and charup:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(
                            username=username,
                            first_name=name,
                            last_name=surname,
                            email=email,
                            password=password1)
                        user.is_active = False
                        user.save()
                        send_activation_email(request, user)
                        messages.success(request, 'Kaydınız başarıyla oluşturuldu. Hesabınızı aktifleştirmek için e-posta adresinizi kontrol edin.')
                        return redirect("Register")
                    else:
                        messages.warning(request, "Bu E-mail adresi kullanılıyor !!!")
                        hata = "email"
                else :
                    messages.warning(request, "Bu Kullanıcı adı kullanılıyor !!!")
                    hata = "username"
            else :
                messages.warning(request, "Şifreniz büyük harf ve sayı içermesi gerekmektedir !!!")
                hata = "password"
        else :
            messages.warning(request, "Şifreler eşleşmiyor !!!")
            hata = "password"
        
        context ={}
        if hata == "email":
            context.update({
                "username":username,
                "name":name,
                "surname":surname,
                "hata":hata,
            })
        elif hata == "username":
            context.update({
                "name":name,
                "surname":surname,
                "email":email,
                "hata":hata,
            })
        elif hata == "password":
            context.update({
                "username":username,
                "name":name,
                "surname":surname,
                "email":email,
                "hata":hata,
            })
        return render(request, 'register.html',context)
    context={}
    return render(request, 'register.html',context)

def send_activation_email(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Hesabınızı Aktifleştirin'
    message = render_to_string('mail/activation_email.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'domain': current_site.domain,
    })
    send_mail(mail_subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=message)

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Hesabınız başarıyla aktifleştirildi. Giriş yapabilirsiniz.')
        return redirect('Login')
    else:
        messages.error(request, 'Geçersiz aktivasyon bağlantısı.')
        return redirect('activation_failure')

def Login(request):
    hata = "" 
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        rememberme = request.POST.get("rememberme")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            if rememberme == "on":
                request.session.set_expiry(None)

            else :
                request.session.set_expiry(0)
            login(request, user)
            messages.success(request, "Giriş başarılı,\n{} {}".format(request.user.first_name, request.user.last_name))
            return redirect('Index')

        else:
            messages.warning(request, "Kullanıcı adı veya " + '\nşifre yanlış !!!')
            hata = "user-password"

    else:
        if not request.user.is_anonymous:
            logout(request)

    context ={"hata":hata}
    return render(request, "login.html", context)

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user :
            current_site = get_current_site(request)
            mail_subject = 'Parola Hatırlatma'
            message = render_to_string('mail/reset_password.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'domain': current_site.domain,
        })
            send_mail(mail_subject, '', settings.EMAIL_HOST_USER, [email], html_message=message)
            messages.success(request,'Şifre sıfırlama linkini E-Posta adresinize gönderilmiştir.')
        else :
            messages.warning(request,'Girmiş olduğunuz mail adresi sistemimizde kayıtlı değildir. Kontrol ederek tekrar deneyiniz.')
        
        return redirect('forgotpassword.html')
    return render(request, 'forgotpassword.html')


def RenewPassword(request, uidb64, token):
    hata = ""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method=="POST":
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if new_password1 == new_password2:
                if new_password1 and new_password2 != " ":
                    charup = False
                    charnum = False
                    for char in new_password1:
                        if char.isupper():
                            charup = True
                        if char.isnumeric():
                            charnum = True
                    if charnum and charup:
                        user.set_password(new_password1)
                        user.save()
                        print(new_password1)
                        messages.success(request,'Şifreniz başarılı olarak değişmiştir. \n Tekrar giriş yapınız ')
                        return redirect('Login')
                    else:
                        messages.warning(request, "Şifreniz büyük harf ve sayı içermesi gerekmektedir !!!")
                        hata = "new-password-error"

                else:
                    messages.warning(request,'Yeni şifre kısmı boş bırakılamaz')
                    hata = "new-password-error"

            else:
                messages.warning(request,'Şifreler birbiri ile uyuşmuyor')
                hata = "new-password-error"
        context ={"hata":hata}
        return render(request, 'renew_password.html', context)
    else:
        messages.error(request, 'Geçersiz şifre sıfırlama bağlantısı.')
        return redirect('Login')


def Logout(request):
    messages.success(request, "Çıkış başarılı, \n Yine bekleriz {}".format(request.user.first_name))
    logout(request)

    return redirect("Login")

