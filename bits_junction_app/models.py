from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    creation_date = models.DateTimeField(default=datetime.utcnow)
    due_date = models.DateTimeField(default=datetime.utcnow)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['-creation_date']

class Question(models.Model):
    MULTIPLE_CHOICE = 'MC'
    SINGLE_CHOICE = 'SC'
    CHOICE_TYPES = (
            (MULTIPLE_CHOICE, 'Multiple Choice'),
            (SINGLE_CHOICE, 'Single Choice'),
        )
    quiz = models.ForeignKey(Quiz)
    question_text = RichTextField()
    creation_date = models.DateTimeField(default=datetime.utcnow)
    type = models.CharField(max_length=2,
                choices=CHOICE_TYPES,
                default=SINGLE_CHOICE)

    def __unicode__(self):
        return self.question_text
    
    class Meta:
        ordering = ['creation_date']

class Option(models.Model):
    question = models.ForeignKey(Question)
    order = models.SmallIntegerField(default=-1)
    option_text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.option_text

    class Meta:
        ordering = ['order']