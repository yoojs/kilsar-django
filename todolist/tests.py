from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Todo, TodoItem

class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.todo = Todo.objects.create(
            title='Test Todo',
            desc='Test Description',
            owner=self.user
        )
        self.todo_item = TodoItem.objects.create(
            desc='Test Item',
            todo_list=self.todo,
            owner=self.user,
            order=1
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.desc, 'Test Description')
        self.assertEqual(self.todo.owner, self.user)

    def test_todo_item_creation(self):
        self.assertEqual(self.todo_item.desc, 'Test Item')
        self.assertEqual(self.todo_item.todo_list, self.todo)
        self.assertEqual(self.todo_item.order, 1)
        self.assertFalse(self.todo_item.is_complete)

class TodoAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            title='Test Todo',
            desc='Test Description',
            owner=self.user
        )

    def test_create_todo(self):
        url = '/api/todo/'
        data = {
            'title': 'New Todo',
            'desc': 'New Description',
            'owner': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.get(title='New Todo').desc, 'New Description')

    def test_create_todo_item(self):
        url = f'/api/todo/{self.todo.id}/items/'
        data = {
            'desc': 'New Todo Item',
            'todo_list': self.todo.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoItem.objects.count(), 1)
        self.assertEqual(TodoItem.objects.first().desc, 'New Todo Item')

    def test_todo_item_ordering(self):
        # Create multiple items
        TodoItem.objects.create(
            desc='Item 1',
            todo_list=self.todo,
            owner=self.user,
            order=1
        )
        TodoItem.objects.create(
            desc='Item 2',
            todo_list=self.todo,
            owner=self.user,
            order=2
        )
        # Test reordering
        url = f'/api/todo/{self.todo.id}/items/2/'
        data = {'order': 2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify order changed
        items = TodoItem.objects.filter(todo_list=self.todo).order_by('order')
        self.assertEqual(items[0].desc, 'Item 2')
        self.assertEqual(items[1].desc, 'Item 1')
