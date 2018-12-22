from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required #decorator personalizado

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

@login_required
def undo_enrollment(request, slug):
	course = get_object_or_404(Course, slug=slug)
	enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
	if request.method == 'POST':
		enrollment.delete()
		messages.success(request, 'Sua inscrição foi cancelada!')
		return redirect('dashboard')
	template = 'courses/undo_enrollment.html'
	context = {
		'enrollment':enrollment,
		'course':course
	}
	return render(request, template, context)

@login_required
@enrollment_required #decorator personalizado
def announcements(request, slug):
	course = request.course

	template = 'courses/announcements.html'
	context = {
		'course':course,
		'announcements': course.announcements.all()
	}
	return render(request, template, context)

@login_required
@enrollment_required #decorator personalizado
def show_announcements(request, slug, pk):
	course = request.course

	announcement = get_object_or_404(course.announcements.all(), pk=pk)	
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False) #apenas para criar o objeto e retorná-lo sem estar salvo, caso haja commit=False
		comment.user = request.user
		comment.announcement = announcement
		comment.save() # sem o commit=False o método salva o objeto
		form = CommentForm() #somente para zerar o formulário
		messages.success(request, 'Seu comentário foi enviado.')
	template = 'courses/show_announcement.html'

	context = {
		'course':course,
		'announcement':announcement,
		'form':form,
	}
	return render(request, template, context)

@login_required
@enrollment_required
def lessons(request, slug):
	course = request.course
	template = 'courses/lessons.html'
	lessons = course.release_lessons()
	if request.user.is_staff:
		lessons = course.lessons.all() #permite acesso a todas as aulas ao staff
	context = {
		'course': course,
		'lessons': lessons,
	}
	return render(request, template, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
	course = request.course
	lesson = get_object_or_404(Lesson, pk=pk, course=course)
	#por questões de segurança faço as seguintes restrições
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Esta aula não está disponível.')
		return redirect('lessons', slug=course.slug)

	template = 'courses/lesson.html'
	context = {
		'course': course,
		'lesson': lesson,
	}
	return render(request, template, context)

@login_required
@enrollment_required
def material(request, slug, pk):
	course = request.course
	material = get_object_or_404(Material, pk=pk, lesson__course=course) #__ acessa propriedade do outro objeto
	lesson = material.lesson
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Esse material não está disponível.')
		return redirect('lesson', slug=course.slug, pk=lesson.pk)
	if not material.is_embedded():
		return redirect(material.file.url) #considerando que existe um arquivo para baixar, caso contrário vai dar erro
	template = 'courses/material.html'
	context = {
		'course': course,
		'lesson': lesson,
		'material': material,
	}
	return render(request, template, context)