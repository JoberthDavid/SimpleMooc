from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment
from .forms import ContactCourse

def courses(request):
	courses = Course.objects.all()
	template_name = 'courses/index.html'
	context = {'courses':courses}
	return  render(request, template_name, context)

#def details(request, pk): utilizando a pk para encontrar o objeto
#	course = get_object_or_404(Course, pk=pk)
#	template_name = 'courses/details.html'
#	context = {
#		'course':course
#	}
#	return render(request, template_name, context)

def details(request, slug): #utilizando o slug para encontrar o objeto
	is_valid=False
	course = get_object_or_404(Course, slug=slug)
	template_name = 'courses/details.html'
	if request.method == 'POST':
		form = ContactCourse(request.POST) #se request for post atribue os valores submetidos pelo usuário
		if form.is_valid(): #se formulário for válido indica uma variável com valor True
			is_valid=True
			form.send_mail(course)
			form = ContactCourse()
	else:
		form = ContactCourse() #do contrário cria uma instância vazia do formulário
	context = {
		'is_valid':is_valid,
		'course':course,
		'form':ContactCourse()
	}
	return render(request, template_name, context)

@login_required
def enrollment(request, slug): #view para inscrição
	course = get_object_or_404(Course, slug=slug)
	enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
	if created:
		enrollment.active()
		messages.success(request, 'Inscrição realizada com sucesso!')
	else:
		messages.info(request, 'Você já está inscrito nesse curso.')
	return redirect('dashboard')