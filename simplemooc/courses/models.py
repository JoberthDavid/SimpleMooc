from django.db import models
from django.urls import reverse

from django.conf import settings

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

class Enrollment(models.Model):

	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)

	#chave estrangeira para usuário devo usar settings.AUTH_USER_MODEL
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='enrollments', on_delete=models.CASCADE) #related_name é um atributo criado no usuário para relacionamento com a tabela usuário
	course = models.ForeignKey(Course, verbose_name='Curso', related_name='enrollments', on_delete=models.CASCADE)
	status = models.IntegerField(verbose_name='Situação', choices=STATUS_CHOICES, default=0, blank=True)
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	update_at = models.DateField('Atualizado em ', auto_now=True)

	def active(self):
		self.status = 1
		self.save()


	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = ( ('user', 'course') ) #para esse model o django vai criar um índice de unicidade combinando dois ou mais campos, de modo que só tenha uma inscrição para um usuário em um curso
