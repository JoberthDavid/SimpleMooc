from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.courses, name='cursos'),
	#path('<int:pk>/', views.details, name='details') utilizando o pk
	path('<slug:slug>/', views.details, name='details')
]