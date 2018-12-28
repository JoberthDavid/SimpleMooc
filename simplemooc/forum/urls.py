from django.urls import path, include
from .views import *

from . import views

urlpatterns = [
	path('', ForumView.as_view(), name='forum'),
	path('<tag>', ForumView.as_view(), name='forum'),
	path('topico/<slug:slug>', ThreadView.as_view(), name='thread'),
	path('respostas/<int:pk>/correta', ReplyCorrectView.as_view(), name='correct'),
	path('respostas/<int:pk>/incorreta', ReplyCorrectView.as_view(correct=False), name='incorrect'),
]