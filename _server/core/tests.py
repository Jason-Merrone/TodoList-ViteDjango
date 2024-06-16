from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Todo_Item

class TodoListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.todo1 = Todo_Item.objects.create(user=self.user, content='Test todo 1', due_date='2024-06-16')
        self.todo2 = Todo_Item.objects.create(user=self.user, content='Test todo 2', due_date='2024-06-17')

    def test_get_todos(self):
        url = reverse('get_todos')  # Assuming your URL pattern name is 'get_todos'
        self.client.force_login(self.user)  # Log in the user for the test
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        data = response.json()
        print(data)
        self.assertIn('Todos', data)  # Check if the response contains a 'Todos' key
        todos_data = data['Todos']
        self.assertEqual(len(todos_data), 2)  # Check if both todos are returned
        self.assertEqual(todos_data[0]['content'], 'Test todo 2')  # Check the order of todos
        self.assertEqual(todos_data[1]['content'], 'Test todo 1')

    def tearDown(self):
        # Clean up after the test
        Todo_Item.objects.all().delete()
        User.objects.all().delete()
