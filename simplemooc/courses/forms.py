from django import forms
from django.core.mail import send_mail #função do Django para o envio de email
from django.conf import settings #importa todos os arquivos de configuração do django

from simplemooc.core.mail import send_mail_template #para importar a função de envio de email html da app Core

class ContactCourse(forms.Form):

	name = forms.CharField(label='Nome', max_length=100)
	email = forms.EmailField(label='email')
	message = forms.CharField(label='Mensagem', widget=forms.Textarea) #não é textfield porque no forms.Form não existe, daí a necessidade do atributo widget no charfield

	def send_mail(self, course):

		subject = '[%s] contato' % course
		message = 'Nome: %(name)s; email: %(email)s; %(message)s'
		context = {
			'name': self.cleaned_data['name'],
			'email': self.cleaned_data['email'],
			'message': self.cleaned_data['message'],
		}
		#segue forma de enviar email somente como texto
		#message = message % context
		#send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
		
		#segue a forma de enviar email html
		template_name = 'courses/contact_email.html'
		send_mail_template( subject, template_name, context, [settings.CONTACT_EMAIL])