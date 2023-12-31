from rest_framework.routers import DefaultRouter
from django.urls import path
from course.views import *

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('payments/', PaymentsListView.as_view(), name='payments_list'),
    path('lessoen/<int:pk>/', LessonDetailView.as_view(), name='lesson_Detail'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payment/<str:payment_id>/', GetPaymentView.as_view(), name='payment_get'),
    path('course/create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('lesson/<int:pk>/update', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete', LessonDeleteView.as_view(), name='lesson_delete'),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/<int:pk>/update', SubscriptionUpdateView.as_view(), name='subscription_update'),
              ] + router.urls
