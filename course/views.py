from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from course.models import Course, Lesson, Payments, SubscriptionCourse
from course.permissions import IsModerator
from course.serializers.serializers import CourseSerializers, LessonSerializers, PaymentsSerializers, \
    SubscriptionCourseSerializers
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from course.services import course_update
from users.models import UserRoles


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer) -> None:
        """Сохраняет новому объекту владельца"""
        serializer.save(owner=self.request.user)

    # def perform_update(self, serializer):
    #     """Сохраняет объект и отправляет письмо"""
    #     self.object = serializer.save()
    #     course_update(self.object)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)

    def perform_create(self, serializer) -> None:
        """Сохраняет новому объекту владельца"""
        serializer.save(owner=self.request.user)

    # def post(self, request, *args, **kwargs):
    #
    #     """В этом коде мы создаем копию объекта request.data с помощью метода copy(). Затем мы вносим изменения в эту
    #     копию, присваивая request.user.id в поле 'user'. После этого мы передаем измененные данные в метод create()
    #     для создания урока."""
    #
    #     data = request.data.copy()
    #     data['owner'] = request.user.id
    #     return self.create(data, *args, **kwargs)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)

    # def post(self, request, *args, **kwargs):
    #
    #     """В этом коде мы создаем копию объекта request.data с помощью метода copy(). Затем мы вносим изменения в эту
    #     копию, присваивая request.user.id в поле 'user'. После этого мы передаем измененные данные в метод create()
    #     для создания урока."""  _____или нет)____
    #
    #     data = request.data.copy()
    #     data['owner'] = request.user.id
    #     return self.create(data, *args, **kwargs)


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class PaymentsListView(generics.ListAPIView):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_type', 'course', 'lesson']
    filterset_class = FilterSet
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]

"""Фильтрация для эндпоинтов вывода списка платежей с возможностями:
менять порядок сортировки по дате оплаты,
фильтровать по курсу или уроку,
фильтровать по способу оплаты."""


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionCourseSerializers
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionCourseSerializers
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]

