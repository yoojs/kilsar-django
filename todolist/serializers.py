from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer
from todolist.models import Todo, TodoItem

class TodoItemSerializer(ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'desc', 'is_complete', 'order', 'owner','todo_list')
class TodoSerializer(ModelSerializer):
    todo_items = TodoItemSerializer(source='todoitem_set', many=True, read_only=True)
    class Meta:
        model = Todo
        fields = ('id', 'title', 'desc','owner', 'todo_items',)
