from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, Enrollment

#implementação de um decorator personalizado para 

def enrollment_required(view_func): # função que recebe uma view

	def _wrapper(request, *args, **kwargs): #args e kwargs são parâmetros genéricos que deverão ser nomeados

		slug = kwargs['slug'] #deve ter um slug do curso na url
		course = get_object_or_404(Course, slug=slug) #busca o curso atual
		has_permission = request.user.is_staff #se o usuário for staff tem acesso imediato, caso contrário devem ser feitas verificações

		if not has_permission: # caso não seja staff

			try: #tenta buscar a inscrição no curso
				enrollment = Enrollment.objects.get(user=request.user, course=course)

			except Enrollment.DoesNotExist: #caso não esteja inscrito
				message = 'Descuple, mas você não tem permissão para acessar essa página.'

			else: # caso não seja staff, mas tenha uma inscrição
				if enrollment.is_approved(): #verifica se a inscrição está aprovada
					has_permission=True
				else:
					message = 'A sua inscrição no curso está pendente.'

		if not has_permission: #verifica se de fato tem permissão
			messages.error(request, message) #caso não tenha permissão emite mensagem de erro
			return redirect('dashboard')

		request.course = course #caso tenha permissão lança o course no request e toda vez que usar esse decorator terá o course no request

		return view_func(request, *args, **kwargs)
	return _wrapper