from django.shortcuts import render

from django.views.generic import TemplateView, View, ListView

from .models import Thread

#class based view
#class ForumView(TemplateView):

#	template_name = 'forum/index.html'

#ListView para listar objetos de um model
class ForumView(ListView):

	model = Thread
	paginate_by = 10 #para paginar de 10 em 10 no template
	template_name = 'forum/index.html'