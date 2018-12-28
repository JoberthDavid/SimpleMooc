from django.db import models
from django.urls import reverse
from django.conf import settings

from taggit.managers import TaggableManager


class Thread(models.Model):

	title = models.CharField('Título', max_length=100)
	slug = models.SlugField('Identificador', max_length=100, unique=True)
	body = models.TextField('Mensagem')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads', on_delete=True)
	
	#serve para contar a quantidade de visualizações e fazer a ordenação por esse número
	views = models.IntegerField('Visualizações', blank=True, default=0)
	
	#serve para contar a quantidade de respostas e fazer a ordenação por esse número
	answer = models.IntegerField('Respostas', blank=True, default=0)

	#vem da app taggit para gerar tags de busca
	tags = TaggableManager()

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em ', auto_now=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('thread', kwargs={'slug': self.slug})

	class Meta:
		verbose_name = 'Tópico'
		verbose_name_plural = 'Tópicos'
		ordering = ['-updated_at']


class Reply(models.Model):

	thread = models.ForeignKey(Thread, verbose_name='Tópico', related_name='replies', on_delete=True)
	reply = models.TextField('Resposta')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='replies', on_delete=True)
	correct = models.BooleanField('Correta ?', blank=True, default=False)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em ', auto_now=True)

	def __str__(self):
		return self.reply[:100] #filtro traz apenas as 100 primeiras letras

	class Meta:
		verbose_name = 'Resposta'
		verbose_name_plural = 'Respostas'
		ordering = ['-correct','created_at']

#método para incrementar o contador de respostas por meio de um signal
def post_save_reply(instance, **kwargs):
	instance.thread.answer = instance.thread.replies.count()
	instance.thread.save()
	#o código abaixo não dispara o gatilho do signal por ser um update, no caso ele atribue Falso a todas as respostas exceto a própria
	if instance.correct:
		instance.thread.replies.exclude(pk=instance.pk).update(correct=False)

#método para decrementar o contador de respostas por meio de um signal
def post_delete_reply(instance, **kwargs):
	instance.thread.answer = instance.thread.replies.count()
	instance.thread.save()

models.signals.post_save.connect(post_save_reply, sender=Reply, dispatch_uid='post_save_reply')
models.signals.post_delete.connect(post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply')