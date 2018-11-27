from django.template import Library #para registrar as tags

#as templatestags são utilizadas quando é necessário uma mesma variável para várias views
#por exemplo todos os cursos do usuário devem estar nas views de painel e de edição de conta

register = Library()

from simplemooc.courses.models import Enrollment

#converte a função em uma tag e utiliza um html para renderizar o resultado
@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
	enrollments = Enrollment.objects.filter(user=user)
	context = {
		'enrollments':enrollments
	}
	return context