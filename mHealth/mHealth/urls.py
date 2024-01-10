"""
URL configuration for mHealth project.

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
from login import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.SignupPage,name='signup'),
    path('', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
     path('sheet/', views.SheetPage, name='sheet'),
    path('logout/', views.LogoutPage, name='logout'),
    path('download-csv/', views.download_csv_data, name='download_csv_data'),
    path('generate_hl7/', views.generate_hl7, name='generate_hl7'),
     path('download_hl7/', views.download_hl7, name='download_hl7'),
     

]
