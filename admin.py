from django.contrib import admin

from quiz.models import  Quiz, MultipleChoiceAnswer, MultipleChoice, Category


class QuizAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	
	radio_admin_fields = {'status': admin.VERTICAL}
	
	list_display = ('title', 'published', 'status',)
	list_filter = ('published', 'status',)
	search_fields = ('title', 'description',)
	filter_vertical = ('questions',)

class MultipleChoiceAdmin(admin.ModelAdmin):
	filter_vertical = ('choices','correct_answer',)
	prepopulated_fields = {'slug': ('question',)}

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Quiz, QuizAdmin)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(MultipleChoice, MultipleChoiceAdmin)
admin.site.register(Category, CategoryAdmin)
