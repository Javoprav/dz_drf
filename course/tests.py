from rest_framework.test import APITestCase
from rest_framework import status
from course.models import Course, Lesson
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

    def test_list_course(self):
        """Тест списка модели Course"""
        self.test_course_create()
        response = self.client.get('/api/course/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'name':\
            'course_for_test', 'preview': None, 'description': None, 'all_lessons': [], 'number_of_lesson': 0,\
            'sub_status': False}]})
        self.assertEqual(Course.objects.all().count(), 1)

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
        response = self.client.post('/api/lesson/create/', {'course': 1, 'name': self.test_model_name, 'owner': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response2 = self.client.post('/api/lesson/create/', {'course': 1, 'name': self.test_model_name, 'url_video': 'yandex.ru', 'owner': 1})
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_lesson(self):
        """Тест деталей модели Lesson"""
        self.test_lesson_create()
        response = self.client.get(f'/api/lesson/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'name': 'Lesson_for_test', 'description': None, 'preview': None, 'url_video': None, 'course': 1, 'owner': 1})

    def test_list_lesson(self):
        """Тест списка модели Lesson"""
        self.test_lesson_create()
        response = self.client.get('/api/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())
        self.assertEqual(response.json(), {'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'name': 'Lesson_for_test', 'description': None, 'preview': None, 'url_video': None, 'course': 1, 'owner': 1}]})
        self.assertEqual(Lesson.objects.all().count(), 1)


class SuperuserTestCase(APITestCase):
    """Тесты суперюзера"""

    def setUp(self) -> None:
        """Подготовка данных перед тестом"""
        self.superuser = User.objects.create(
                        email='superuser@user.com',
                        is_staff=False,
                        is_superuser=True,
                        is_active=True,
                        role=UserRoles.MEMBER,
                    )
        self.superuser.set_password('123')
        self.superuser.save()
        response = self.client.post('/api/token/', {"email": "superuser@user.com", "password": "123"})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.test_model_name = 'Lesson_for_test'
        self.response_course = self.client.post('/api/course/create/', {'name': self.test_model_name})

    def test_lesson_create(self):
        """Тест суперюзера"""
        response = self.client.post('/api/lesson/create/', {'course': 1, 'name': self.test_model_name, 'owner': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response2 = self.client.get('/api/lesson/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
