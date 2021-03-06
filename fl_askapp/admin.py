from django.contrib import admin
from fl_askapp import models
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	list_display=('title', 'id',)
class AnswerAdmin(admin.ModelAdmin):
	list_display=('text',)
class TagAdmin(admin.ModelAdmin):
	list_display=('text',)
class ProfileAdmin(admin.ModelAdmin):
	list_display=('user',)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Profile, ProfileAdmin)
