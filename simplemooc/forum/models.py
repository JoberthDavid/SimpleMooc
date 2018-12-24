from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


class Thread(models.Model):

	title = models.CharField('Título', max_length=100)
	body = models.TextField('Mensagem')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads', on_delete=True)
	
	#serve para contar a quantidade de visualizações e fazer a ordenação por esse número
	views = models.IntegerField('Visualizações', blank=True, default=0)
	
	#serve para contar a quantidade de respostas e fazer a ordenação por esse número
	answer = models.IntegerField('Respostas', blank=True)

	#vem da app taggit para gerar tags de busca
	tags = TaggableManager()

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	update_at = models.DateField('Atualizado em ', auto_now=True)


	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Tópico'
		verbose_name_plural = 'Tópicos'
		ordering = ['-update_at']


class Reply(models.Model):

	thread = models.ForeignKey(Thread, verbose_name='Tópico', related_name='replies', on_delete=True)
	reply = models.TextField('Resposta')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='replies', on_delete=True)
	correct = models.BooleanField('Correta ?', blank=True, default=False)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	update_at = models.DateField('Atualizado em ', auto_now=True)

	def __str__(self):
		return self.reply[:100] #filtro traz apenas as 100 primeiras letras

	class Meta:
		verbose_name = 'Resposta'
		verbose_name_plural = 'Respostas'
		ordering = ['-correct','created_at']