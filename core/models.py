from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True,)
    def __str__(self):
        return f"{self.name} | {self.user}"
    
class GroupName(models.Model):
    group_name = models.CharField(max_length=255, default='others')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} | {self.group_name}"
    
class VocabularyWord(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    definition = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_by = models.ForeignKey(GroupName, on_delete=models.CASCADE, blank=True, null=True)



    def __str__(self):
        return f"{self.word} | {self.definition}"


class UserAnswer(models.Model):
    vocabulary_word = models.ForeignKey(VocabularyWord, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True,)

    def __str__(self):
        return f"{self.vocabulary_word.word} | {self.vocabulary_word.definition}"


