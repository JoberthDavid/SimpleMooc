from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegisterForm, EditAccountForm, PasswordResetForm #importa RegisterForm do arquivo criado em accounts forms.py
from .models import PasswordReset
from simplemooc.core.utils import generate_hash_key

User = get_user_model()

def register(request):
	template_name = 'accounts/register.html'
	if request.method == 'POST':
		form = RegisterForm(request.POST) #cria instância de RegisterForm com a requisição realizada
		if form.is_valid(): #caso o formulário seja válido
			user = form.save() #método save do UserCreationForm
			user = authenticate(username=user.username, password=form.cleaned_data['password1'])
			login(request, user) #efetua login após registro
			return redirect('home')
	else:
		form = RegisterForm() #caso não seja método POST cria um formulário
	context = {'form':form}
	return render(request, template_name, context)

@login_required
def do_logout(request):
	logout(request)
	return redirect('home')

@login_required
def dashboard(request):
	template_name = 'accounts/dashboard.html'
	return render(request, template_name)

@login_required
def edit(request):
	template_name = 'accounts/edit.html'
	success=False
	if request.method == 'POST':
		form = EditAccountForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			form = EditAccountForm(instance=request.user)
			success=True
	else:
		form = EditAccountForm(instance=request.user)
	context={
		'success':success,
		'form':form
	}
	return render(request, template_name, context)

@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	success=False
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			success=True
	else:
		form = PasswordChangeForm(user=request.user)
	context = {
		'success':success,
		'form':form
	}
	return render(request, template_name, context)

def password_reset(request):
	template_name = 'accounts/password_reset.html'
	success=False
	#ao invés de fazer if request.method == 'POST' faremos request.POST or None como abaixo, pois assim o Django não vai validar no caso de ser vazio
	form = PasswordResetForm(request.POST or None)
	if form.is_valid():
		user = User.objects.get(email=form.cleaned_data['email']) #busca o usuário com o get_user_model
		key = generate_hash_key(user.username)#cria a chave pelo método generate_key do arquivo utils.py dentro do app Core. Observe que o parâmetro salt do método foi indicado como user.username, mas poderia ser algum outro parâmetro do usuário
		reset = PasswordReset(key=key, user=user) #cria o objeto PasswordReset
		reset.save() #salva o objeto PasswordReset no banco de dados
		success=True
	context = {
		'success':success,
		'form':form
	}
	return render(request, template_name, context)