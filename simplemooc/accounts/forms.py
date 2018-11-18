from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model #importa a classe que vai chamar o custom user

User = get_user_model() #indica para o Django utilizar nosso custom user

class RegisterForm(forms.ModelForm): #herda de forms.ModelForm ao invés de UserCreationForm

	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)
	
	def clean_password2(self): # método extraído do UserCreationForm do Django que precisa ser reescrito para manter compatibilidade
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2: #verifica se a senha e confirmação foram enviadas e se são iguais
			raise forms.ValidationErro('A confirmação não está correta', code='password_mismatch',) # comando raise significa gerar é usado no tratamento de exceções do Django

	def save(self, commit=True): #este método save sobrescreve o save de UserCreationForm
		user = super(RegisterForm, self).save(commit=False) #o super chama o save de UserCreationForm, mas o commit False não vai salvar o user e dá a possibilidade de alterar o formulário como na linha abaixo
		user.set_password(self.cleaned_data['password1']) # o método set_password criptografa a senha, enquanto o cleaned_data valida um dicionário de dados e passa os valores corretos
		if commit:
			user.save()
		return user

	class Meta:
		model = User
		fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):
	# para não precisar copiar todos os campos do model utiliza-se a classe Meta com o atributo model
	# e os campos que o usuário pode alterar
	class Meta:
		model = User
		fields = ['username', 'email', 'name']

class PasswordResetForm(forms.Form): #não precisa ser um model porque não precisa salvar
	email = forms.EmailField(label='email')

	def clean_email(self): #método para validar se o email está cadastrado no sistema
		email = self.cleaned_data['email']	
		if User.objects.filter(email=email).exists():
			return email
		raise forms.ValidationError('Nenhum usuário encontrado com esse email')
