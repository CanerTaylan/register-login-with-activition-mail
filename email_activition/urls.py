"""
URL configuration for email_activition project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account.views import *
from django.conf import settings  
from django.conf.urls.static import static   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='Index'),
    path('register.html',Register , name='Register'),
    path('login.html',Login , name='Login'),
    path('logout.html',Logout , name='Logout'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('forgotpassword.html',ForgotPassword , name='ForgotPassword'),
    path('renew_password/<str:uidb64>/<str:token>/', RenewPassword, name='RenewPassword'),

] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
