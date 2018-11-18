from django.db import models
from django.urls import reverse


class CourseManager(models.Manager): #custom manager para adicionar algum método além dos métodos do manager padrão do django
	
	def search(self, query): #método criado para encontrar uma queryset a partir de um parâmetro
		return self.get_queryset().filter(models.Q(name__icontains=query) | models.Q(description__icontains=query)) #icontains é um lookup do django

class Course(models.Model):

	name = models.CharField('Nome', max_length=100)
	slug = models.SlugField('Atalho') #slug é uma espécie de atalho
	description = models.TextField('Descrição', blank=True) #não é obrigatório
	about = models.TextField('Sobre o curso', blank=True)
	start_date = models.DateField('Data de início', null=True, blank=True) #campo pode ser vazio
	image = models.ImageField(upload_to='courses/images', null=True, blank=True, verbose_name='Imagens') #o campo do tipo de imagem na verdade é só o caminho salvo no banco para a imagem
	created_at = models.DateTimeField('Criado em', auto_now_add=True) #toda vez que for criado a data e hora é salva
	update_at = models.DateTimeField('Atualizado em', auto_now=True) #toda vez que for salvo a data e hora é alterada

	def __str__(self): #retorna a representação string dos objetos tipo Course
		return self.name

	def get_absolute_url(self): #é um método sugerido pelo Django para retornar a url
		return reverse('details', kwargs={'slug':self.slug}) #retorna uma tupla com a url, segundo parâmetro como argumentos não nomeáveis, o terceiro com argumentos nomeáveis no caso o slug

	class Meta: #
		verbose_name = 'curso'
		verbose_name_plural = 'cursos'
		ordering = ['name'] #ordenação padronizada com que o django vai mostrar, se colocar o sinal negativo ante do name o django faria em ordem decrescente

	objects = CourseManager() #informa que o CourseManager passa a ser o manager utilizado ao invés do padrão do django