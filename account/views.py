from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages



# Create your views here.
def index(request):
    context={
        "title":"Anasayfa",

    }
    return render(request, 'index.html',context)

def Register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
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
                        return redirect("Login")
                    else:
                        messages.warning(request, "Bu E-mail adresi kullanılıyor !!!")
                        hata = "email"
                else :
                    messages.warning(request, "Bu Kullanıcı adı kullanılıyor !!!")
                    hata = "username"
            else :
                messages.warning(request, "Şifreniz büyük harf ve sayı içermesi gerekmektedir !!!")
                hata = "passworda"
        else :
            messages.warning(request, "Şifreler eşleşmiyor !!!")
            hata = "passwordb"
        
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
        elif hata == "passworda":
            context.update({
                "username":username,
                "name":name,
                "surname":surname,
                "email":email,
                "hata":hata,
            })
        elif hata == "passwordb":
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


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Giriş başarılı,\n{} {}".format(request.user.first_name, request.user.last_name))
            return redirect('Index')
        else:
            messages.warning(request, "Kullanıcı adı veya şifre yanlış !!!")
            return redirect('Login')
    
    return render(request, "login.html")



def Logout(request):
    logout(request)
    return redirect("Login")

