from django.contrib import admin
from .models import VocabularyWord, UserAnswer, Subject, GroupName


# Register your models here.

admin.site.register(VocabularyWord)
admin.site.register(UserAnswer)
admin.site.register(Subject)
admin.site.register(GroupName)

