from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Task
from .serializers import TaskSerializer


class TaskSerializerTests(TestCase):
    def test_accepts_lowercase_status_and_priority(self):
        data = {
            'title': 'Write API docs',
            'description': 'Document the task endpoints',
            'status': 'pending',
            'priority': 'high',
            'due_date': '2026-07-10',
            'tags': ['docs', 'backend'],
            'position': 1,
        }

        serializer = TaskSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['status'], 'TODO')
        self.assertEqual(serializer.validated_data['priority'], 'HIGH')


class GlobalResponseTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_validation_errors_use_standard_response(self):
        response = self.client.post('/tasks/', {'title': ''}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Task creation failed')
        self.assertIn('errors', response.data)


class TaskViewSetTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_task_returns_standard_success_response(self):
        payload = {
            'title': 'Write API docs',
            'description': 'Document the task endpoints',
            'status': 'TODO',
            'priority': 'HIGH',
            'due_date': '2026-07-10',
            'tags': ['docs', 'backend'],
            'position': 1,
        }

        response = self.client.post('/tasks/', payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Task created successfully')
        self.assertIn('id', response.data['data'])

    def test_list_filters_by_title_and_date(self):
        Task.objects.create(
            user=self.user,
            title='Alpha task',
            description='First task',
            status='TODO',
            priority='HIGH',
            due_date='2026-07-10',
            tags=['work'],
            position=1,
        )
        Task.objects.create(
            user=self.user,
            title='Beta task',
            description='Second task',
            status='TODO',
            priority='HIGH',
            due_date='2026-07-10',
            tags=['work'],
            position=2,
        )
        Task.objects.create(
            user=self.user,
            title='Alpha task',
            description='Third task',
            status='TODO',
            priority='HIGH',
            due_date='2026-07-11',
            tags=['work'],
            position=3,
        )

        response = self.client.get('/tasks/', {'date': '2026-07-10', 'title': 'alpha'}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], 'Alpha task')
