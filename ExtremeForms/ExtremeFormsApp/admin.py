from django.contrib import admin
from .models import Question, QuestionList, Answer

# Register your models here.
admin.site.register(QuestionList)
admin.site.register(Question)
admin.site.register(Answer)