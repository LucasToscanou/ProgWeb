from django.contrib import admin
from django.urls import path
from ExtremeFormsApp import views
from django.urls.conf import include
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from ExtremeForms.views import MeuUpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('security/', views.homeSec , name='sec-home'),
    path('security/register/', views.register , name='register'),
    path('security/login/', LoginView.as_view(template_name='security/login.html') , name='sec-login'),
    path('security/profile/', views.secretPage , name='sec-secretPage'),
    path('security/logout/', views.logout , name='sec-logout'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('sec-home')) , name='logout'),
    path('security/password_change/',
        PasswordChangeView.as_view(
        template_name='security/password_change_form.html', 
        success_url=reverse_lazy('sec-password_change_done'),
        ),
        name='sec-password_change'
    ),
    path('security/password_change_done/',
        PasswordChangeDoneView.as_view(
        template_name='security/password_change_done.html',
        ),
        name='sec-password_change_done'
    ),
    path('security/terminaRegistro/<int:pk>/', 
        MeuUpdateView.as_view(
        template_name='security/user_form.html',
        success_url=reverse_lazy('sec-home'),
        model=User,
        fields=[
        'first_name',
        'last_name',
        'email',
        ],
        ), name='sec-completaDadosUsuario'
    ),

    path('security/password_reset/', PasswordResetView.as_view(
        template_name='security/password_reset_form.html', 
        success_url=reverse_lazy('sec-password_reset_done'),
        html_email_template_name='security/password_reset_email.html',
        subject_template_name='security/password_reset_subject.txt',
        from_email='webmaster@meslin.com.br',
        ), name='password_reset'
    ),
    path('security/password_reset_done/', PasswordResetDoneView.as_view(
        template_name='security/password_reset_done.html',
        ), name='sec-password_reset_done'
    ),
    path('security/password_reset_confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(
        template_name='security/password_reset_confirm.html', 
        success_url=reverse_lazy('sec-password_reset_complete'),
        ), name='password_reset_confirm'
    ),
    path('security/password_reset_complete/', PasswordResetCompleteView.as_view(
        template_name='security/password_reset_complete.html'
        ), name='sec-password_reset_complete'
    ),
    
    path('', include('ExtremeFormsApp.urls')),
]
