from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms.models import inlineformset_factory

from models import Question, Quiz, Option

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(widget=CKEditorWidget())
    type = forms.ChoiceField(choices=Question.CHOICE_TYPES, widget=forms.Select(attrs={'class':'form-control label-type'}))
    quiz = forms.ModelChoiceField(queryset=Quiz.objects.all())
    
    class Meta:
        model = Question
        fields = ('question_text', 'type', 'quiz')
        exclude = ('creation_date',)

class OptionForm(forms.ModelForm):
    option_text = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
#     DELETE = forms.BooleanField(widget=forms.CheckboxInput(attr={'class': 'form-control'}))
    class Meta:
        model = Option
        fields = ('option_text', 'order', 'question')

OptionInlineFormSet = inlineformset_factory(Question, Option, form=OptionForm, extra=0, can_delete=True)