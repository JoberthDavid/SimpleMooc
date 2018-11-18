from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('contato/', views.contact, name='contact')
]