from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from course.models import *
from course.pagination import CoursePagination, LessonPagination
from course.permissions import IsModerator
from course.serializers.serializers import *
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
import requests
from course.services import checkout_session, create_payment
from users.models import UserRoles
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from course.tasks import send_mail_user_update
stripe.api_key = settings.STRIPE_SECRET_KEY


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePagination

    def perform_create(self, serializer) -> None:
        """Сохраняет новому объекту владельца"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        self.object = serializer.save()
        send_mail_user_update.delay(self.object.pk)

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
    pagination_class = LessonPagination

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


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializers
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Создание платежа"""
        # stripe_key = settings.STRIPE_SECRET_KEY
        # course_id = request.data['course']
        # user = request.user
        # course = get_object_or_404(Course, pk=request.data['course'])
        # try:
        #     session = checkout_session(course, user)
        #     create_payment(course, user)
        #     return Response(session['id'])
        # except Exception:
        #     return Response('error',  status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = checkout_session(
            course=serializer.validated_data['course'],
            user=self.request.user
        )
        serializer.save()
        create_payment(course=serializer.validated_data['course'],
                       user=self.request.user)
        return Response(session['id'], status=status.HTTP_201_CREATED)


class GetPaymentView(APIView):
    """Получение информации о платеже"""
    def get(self, request, payment_id):
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        return Response({
            'status': payment_intent.status, })
