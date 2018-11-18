from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('entrar/', auth_views.LoginView.as_view(template_name = 'accounts/login.html'), name='login'), # utilizando o login do Django com sua própria view
    path('sair/', views.do_logout, name='logout'),
	path('cadastre-se/', views.register, name='register'),
	path('painel/', views.dashboard, name='dashboard'),
	path('editar/', views.edit, name='edit'),
	path('editar_senha/', views.edit_password, name='edit_password'),
	path('nova_senha/', views.password_reset, name='password_reset')
]