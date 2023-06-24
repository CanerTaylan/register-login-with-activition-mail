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
                        user.save()
                        send_activation_email(request, user)

                        return redirect("Login")
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
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Giriş başarılı,\n{} {}".format(request.user.first_name, request.user.last_name))
            return redirect('Index')
        else:
            messages.warning(request, "Kullanıcı adı veya " + '\nşifre yanlış !!!')
            hata = "user-password"
    context ={"hata":hata}
    return render(request, "login.html", context)



def Logout(request):
    logout(request)
    return redirect("Login")

