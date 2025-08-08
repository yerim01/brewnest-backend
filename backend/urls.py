"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("store/", include("store.urls")),
    path("accounts/user/register/", UserCreate.as_view(), name="user_create"),
    path("accounts/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"), # regular login
    path("accounts/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("accounts-auth/", include("rest_framework.urls")), # django login
    path("google-auth/", include("allauth.urls")), # google login path
    path("callback/", google_login_callback, name="callback"), # google login redirect URL
    path("accounts/auth/user/", UserDetailView.as_view(), name="user_detail"),
    path("accounts/google/validate_token/", validate_google_token, name="validate_token"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.http import HttpResponseBadRequest

def handler400(request, exception=None):
    return HttpResponseBadRequest("Bad request")
