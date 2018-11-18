from django.contrib import admin

from .models import Course

#
class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'slug', 'start_date', 'created_at'] #faz com que o admin exiba os campos entre colchetes no site Admin
	search_fields = ['name', 'slug'] #cria no admin um field para pesquisar
	prepopulated_fields = {'slug': ('name',)} #faz com que o campo slug seja preenchido automaticamente com o campo nome

admin.site.register(Course, CourseAdmin) #caso exista o admin alterado com uma classe eu devo informar o seu nome como o segundo parâmetro

