from django.shortcuts import render, get_object_or_404

from .models import Course

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
	course = get_object_or_404(Course, slug=slug)
	template_name = 'courses/details.html'
	context = {
		'course':course
	}
	return render(request, template_name, context)