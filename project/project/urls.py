"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from techei.views import register,institution,individual
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('', register.HomeView, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('techei/', include('techei.urls')),
    path('accounts/signup/', register.SignUpView.as_view(), name='signup'),
    path('accounts/login/', register.LoginView.as_view(), name='login'),
    path('accounts/login/home/', register.HomeView, name='home'),
    path('accounts/signup/individual/', individual.IndividualSignUpView.as_view(), name='individual_signup'),
    path('accounts/signup/institution/', institution.InstitutionSignUpView.as_view(), name='institution_signup'),
    path('individual_profile', individual.IndividualProfileView, name='individual_profile'),
    path('institution_profile', institution.InstitutionProfileView, name='institution_profile'),
    path('ajax/load-cities/', individual.load_cities, name='ajax_load_cities'),
    #path('individual_dashboard', individual.IndividualDashboardView, name='individual_dashboard'),
    #path('institution_dashboard', institution.InstitutionDashboardView, name='institution_dashboard'),
    path('accounts/signup/institution/', institution.InstitutionSignUpView.as_view(), name='institution_signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
