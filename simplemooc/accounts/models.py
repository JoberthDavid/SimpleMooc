import re #importa o módulo de validação Regex
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):

	username = models.CharField('Nome de Usuário', max_length=30, unique=True, 
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
			'O nome de usuário só pode conter letras, digitos ou os '
			'seguintes caracteres: @/./+/-/_', 'invalid')]) # o campo validators é uma lista passada para o formulário fazer a validação do valor inserido pelo usuário
	email = models.EmailField('email', unique=True)
	name = models.CharField('Nome', max_length=100, blank=True)
	is_active = models.BooleanField('Está ativo?', blank=True, default=True) #importante pois no usuário padrão do Django existe
	is_staff = models.BooleanField('É da equipe?', blank=True, default=False) #importante para o Django saber se pode acessar o admin
	date_joined = models.DateTimeField('Data de entrada', auto_now_add=True) #importante para deixar compatível com o admin do Django

	objects = UserManager() #manager do Django

	USERNAME_FIELD = 'username' #campo de referência do login
	REQUIRED_FIELDS = ['email'] #campo para criação de usuário

	def __str__(self):
		return self.name or self.username

	def get_short_name(self):
		return self.username

	def get_full_name(self):
		return str(self)

	class Meta:
		verbose_name = 'usuário'
		verbose_name_plural = 'usuários'

#criando uma classe para redefinir senha, poderia ser feito pelo próprio Django
class PasswordReset(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=True, verbose_name='Usuário',
		related_name='resets') #usuário pode ter um ou muitos PasswordReset. Poderia ter colocado accounts.User, mas já foi atribuido esse valor à variável AUTH_USER_MODEL no settings
	# o related_name é para renomear o método PasswordReset_set do Django
	key = models.CharField('Chave', max_length=100, unique=True)
	created_at = models.DateTimeField('Criado em ', auto_now_add=True) #para colocar um prazo para o link a ser enviado ao usuário
	confirmed = models.BooleanField('Confirmado', default=False, blank=True) #sinaliza se o link enviado para reset foi utilizado pelo usuário

	def __str__(self):
		return '{0} em {1}'.format(self.user, self.created_at)

	class Meta:
		verbose_name = 'Nova senha'
		verbose_name_plural = 'Novas senhas'
		ordering = ['-created_at'] #ordena de modo decrescente (observe o sinal de menos antes da variável)a partir da criação