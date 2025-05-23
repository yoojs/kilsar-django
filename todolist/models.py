from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class TodoItem(models.Model):
    desc = models.TextField()
    is_complete = models.BooleanField(default=False, blank=True, null=True)
    order = models.IntegerField(default=1)
    todo_list = models.ForeignKey(to=Todo, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.desc
    class Meta:
        ordering = ['order']