from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo_Item
from django.contrib.auth.models import User

class DeleteTodoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.todo = Todo_Item.objects.create(user=self.user, content='Test Todo', due_date='2024-06-30')

    def test_delete_todo_success(self):
        response = self.client.post(reverse('delete_todo', kwargs={'todo_id': self.todo.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Todo deleted'})

        # Check if the todo item was actually deleted
        with self.assertRaises(Todo_Item.DoesNotExist):
            Todo_Item.objects.get(id=self.todo.id)

    def test_delete_todo_not_found(self):
        response = self.client.post(reverse('delete_todo', kwargs={'todo_id': 999}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Todo not found'})

    def tearDown(self):
        self.client.logout()
