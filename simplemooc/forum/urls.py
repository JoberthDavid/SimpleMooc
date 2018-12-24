from django.urls import path, include
from .views import *

from . import views

urlpatterns = [
	path('', ForumView.as_view(), name='index'),
]