"""autoprint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as users_views
from users.forms import MyLoginView, NewPasswordResetView, NewPasswordResetConfirmView
from users.views import signup, activate, register_success

urlpatterns = [
	path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('login/', MyLoginView.as_view(template_name = 'users/login.html'), name = 'login'),

    # path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('password_reset/', NewPasswordResetView.as_view(
        template_name= 'users/PasswordReset.html'
        ), name='password_reset'),
    path('accounts/reset/<uidb64>/<token>/', NewPasswordResetConfirmView.as_view(
        template_name = 'users/password_reset_confirm2.html'
        ), name='password_reset_confirm' ),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name= 'password_reset_complete'),
    path('register/success/', register_success, name = 'register_success'),
    path('register/', signup, name = 'register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    # path('register/', users_views.register, name = 'register'),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)