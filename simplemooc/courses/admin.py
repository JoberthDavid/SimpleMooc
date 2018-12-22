from django.contrib import admin

from .models import (Course, Enrollment, Announcement, Comment, Lesson, Material)

#
class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'slug', 'start_date', 'created_at'] #faz com que o admin exiba os campos entre colchetes no site Admin
	search_fields = ['name', 'slug'] #cria no admin um field para pesquisar
	prepopulated_fields = {'slug': ('name',)} #faz com que o campo slug seja preenchido automaticamente com o campo nome

#cria um form_set que serve para cadastrar um model, no caso um InLineModelAdmin do tipo Tabular ou Stack
class MaterialInLineAdmin(admin.StackedInline):
	model = Material

class LessonAdmin(admin.ModelAdmin):

	list_display = ['name', 'number', 'course', 'release_date']
	search_fields = ['name', 'description']
	list_filter = ['created_at'] #cria um filtro lateral no admin

	inlines = [
		MaterialInLineAdmin,
	]

admin.site.register(Course, CourseAdmin) #caso exista o admin alterado com uma classe eu devo informar o seu nome como o segundo parâmetro
admin.site.register([Enrollment, Announcement, Comment])
admin.site.register(Lesson, LessonAdmin)