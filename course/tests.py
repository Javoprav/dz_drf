from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, UserRoles


class  CourseTestCase(APITestCase):
    """Тесты модели Course"""
    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(
            email='user@user1.com',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
        )
        self.user.set_password('123')
        self.user.save()
        response = self.client.post('/api/token/', {"email": "user@user1.com", "password": "123"})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.test_model_name = 'course_for_test'

    def test_course_create(self):
        """Тест создания модели Course"""
        response = self.client.post('/api/course/create/', {'name': self.test_model_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_course(self):
        """Тест деталей модели Course"""
        self.test_course_create()
        response = self.client.get(f'/api/course/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'name': 'course_for_test', 'preview': None, 'description': None, 'all_lessons': [], 'number_of_lesson': 0, 'sub_status': False})

class LessonTestCase(APITestCase):
    """Тесты модели Lesson"""

    def setUp(self) -> None:
        """Подготовка данных перед тестом"""
        self.user = User.objects.create(
            email='user@user1.com',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
        )
        self.user.set_password('123')
        self.user.save()
        response = self.client.post('/api/token/', {"email": "user@user1.com", "password": "123"})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.test_model_name = 'Lesson_for_test'
        self.response_course = self.client.post('/api/course/create/', {'name': self.test_model_name})

    def test_lesson_create(self):
        """Тест создания модели Lesson"""
        response = self.client.post('/api/lesson/create/', {'course': 1, 'name': self.test_model_name})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
