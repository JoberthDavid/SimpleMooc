from django.shortcuts import render, redirect, get_object_or_404
#from django.urls import path

from django.views.generic import TemplateView, View, ListView, DetailView
from django.contrib import messages

from .models import Thread, Reply

from .forms import ReplyForm

#class based view
#class ForumView(TemplateView):

#	template_name = 'forum/index.html'

#ListView para listar objetos de um model
class ForumView(ListView):

	#model = Thread #declara o model, porém posso retirar essa declaração e inseri-la no método get_queryset
	paginate_by = 5 #para paginar de 10 em 10 no template
	template_name = 'forum/index.html'

	#para adicionar algo a mais no contexto devo implementar o seguinte método
	#kwargs são parâmetros nomeados passadas na url em classes baseadas em views
	#args são parâmetros não nomeados passados na url em classes baseadas em views
	def get_context_data(self, **kwargs):
		context = super(ForumView, self).get_context_data(**kwargs)
		context['tags'] = Thread.tags.all() #chama todas as tags associadas a Thread
		context['replies'] = Reply.objects.all()
		return context

	#método que declara o model e faz ordenações conforme uma query
	def get_queryset(self):
		queryset = Thread.objects.all()
		queryset_reply = Reply.objects.all()
		order = self.request.GET.get('order','') #request está disponível na instância em casos de views baseadas em classes
		order_reply = self.request.GET.get('order_reply', '')
		if order == 'views':
			queryset = queryset.order_by('-views')
		elif order == 'answers':
			queryset = queryset.order_by('-answer')
		if order_reply == 'updated_at':
			queryset_reply = queryset_reply.order_by('updated_at')
		tag = self.kwargs.get('tag', None)
		if tag:
			queryset = queryset.filter(tags__slug__icontains=tag)
		return queryset

#para essa classe é necessário que o model tenha um slug senão ele utilizará a pk para buscar objetos da classe
class ThreadView(DetailView):

	model=Thread
	template_name = 'forum/thread.html'

	def get(self, request, *args, **kwargs):
		response = super(ThreadView, self).get(request, *args, **kwargs)
		#se o usuário não estiver autenticado ou se ele não for o autor do tópico então conto a visualização
		if not self.request.user.is_authenticated or (self.object.author != self.request.user):
			self.object.views = self.object.views + 1
			self.object.save()
		return response

	def get_context_data(self, **kwargs):
		context = super(ThreadView, self).get_context_data(**kwargs)
		context['tags'] = Thread.tags.all()
		context['form'] = ReplyForm(self.request.POST or None)
		return context

	def post(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			messages.error(self.request, 'Para responder ao tópico é necessário estar logado.')
			return redirect(self.request.path) #redireciona para a mesma url
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		form = context['form']
		if form.is_valid():
			reply = form.save(commit=False)
			reply.thread = self.object
			reply.author = self.request.user
			reply.save()
			messages.success(self.request, 'Sua resposta foi enviada com sucesso.')		
			context['form'] = ReplyForm()
		return self.render_to_response(context)

class ReplyCorrectView(View):

	correct = True

	def get(self, request, pk):
		reply = get_object_or_404(Reply, pk=pk, author=request.user)
		reply.correct = self.correct
		reply.save()
		messages.success(request, 'Comentário atualizado com sucesso.')
		return redirect(reply.thread.get_absolute_url())