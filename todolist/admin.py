from django.contrib import admin
from .models import Todo, TodoItem
# Register your models here.
admin.site.register(Todo)
admin.site.register(TodoItem)