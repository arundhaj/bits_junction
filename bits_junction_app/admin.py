from django import forms
from django.contrib import admin
from models import Quiz, Question, Option
from ckeditor.fields import CKEditorWidget

class OptionInline(admin.TabularInline):
    model = Option
    extra = 0

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'due_date', 'active')

class QuestionAdminForm(forms.ModelForm):
    question_text = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Question
        fields = ['question_text', 'type']
    
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    fieldsets = [
            ('Quiz', {'fields': ['quiz']}),
            ('Question', {'fields': ['question_text', 'type']})
        ]
    inlines = [OptionInline]

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
