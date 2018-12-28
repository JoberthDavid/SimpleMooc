from django.db import models
from django.urls import reverse
from django.utils import timezone

from django.conf import settings

from simplemooc.core.mail import send_mail_template #função importada da app core para enviar email de anúncio com signal

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
	updated_at = models.DateTimeField('Atualizado em', auto_now=True) #toda vez que for salvo a data e hora é alterada

	def __str__(self): #retorna a representação string dos objetos tipo Course
		return self.name

	def get_absolute_url(self): #é um método sugerido pelo Django para retornar a url
		return reverse('details', kwargs={'slug':self.slug}) #retorna uma tupla com a url, segundo parâmetro como argumentos não nomeáveis, o terceiro com argumentos nomeáveis no caso o slug

	def release_lessons(self): #retorna as aulas que estão disponíveis
		today = timezone.now().date() #pega a data de hoje
		return self.lessons.filter(release_date__lte=today) #faz um filtro com release_date e verifica se está no passado (lookup do Dajngo gte futuro e lte no passado)


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
	updated_at = models.DateField('Atualizado em ', auto_now=True)

	def __str__(self):
		return self.user + " - " + self.course

	def active(self):
		self.status = 1
		self.save()

	def is_approved(self):
		return self.status == 1

	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = ( ('user', 'course') ) #para esse model o django vai criar um índice de unicidade combinando dois ou mais campos, de modo que só tenha uma inscrição para um usuário em um curso

class Announcement(models.Model):

	course = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.CASCADE, related_name='announcements')
	title = models.CharField('Título', max_length=100)
	content = models.TextField('Conteúdo')
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateField('Atualizado em ', auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		ordering = ['-created_at']

class Comment(models.Model):

	announcement = models.ForeignKey(Announcement, verbose_name='Ánúncio', related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
	comment = models.TextField('Comentário')
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateField('Atualizado em ', auto_now=True)

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		ordering = ['created_at']

# a função abaixo é um signal parar enviar um email após um anúncio ser criado no banco de dados
def post_save_announcement(instance, created, **kwargs):
	if created: #caso o anúncio tenha sido criado faça
		subject = instance.title
		template_name = 'courses/announcement_mail.html'
		context = {
			'announcement':instance
		}
		enrollments = Enrollment.objects.filter(course=instance.course, status=1)
		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name, context, recipient_list)

#abaixo segue a forma como indicar que a função post_save_announcement é um signal post_save para o model Announcement
models.signals.post_save.connect(post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement') #dispatch_uid verifica se a função post_save_announcement foi cadastrada apenas uma vez para que não ocorram erros

class Lesson(models.Model):

	name = models.CharField('Nome', max_length=100)
	description = models.TextField('Descrição', blank=True)
	number = models.IntegerField('Número (ordem)', blank=True, default=0)
	release_date = models.DateField('Data de liberação', blank=True, null=True)
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)


	course = models.ForeignKey(Course, verbose_name='Curso', on_delete=True, related_name='lessons')

	def __str__(self):
		return self.name

	def is_available(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date <= today
		return False

	class Meta:
		verbose_name = 'Aula'
		verbose_name_plural = 'Aulas'
		ordering = ['number']

class Material(models.Model):

	name = models.CharField('Nome', max_length=100)
	#campo de texto para inserir um embedded, um código para um vídeo do youtube, por exemplo
	embedded = models.TextField('Vídeo embedded', blank=True)
	file = models.FileField(upload_to='lessons/materials', blank=True) #os arquivos dessa forma estão públicos

	lesson = models.ForeignKey(Lesson, verbose_name='aula', on_delete=True, related_name='materials')

	def __str__(self):
		return self.name

	def is_embedded(self):
		return bool(self.embedded)

	class Meta:
		verbose_name = 'Material'
		verbose_name_plural = 'Materiais'