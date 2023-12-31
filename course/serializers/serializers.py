from rest_framework import serializers
from course.models import Course, Lesson, Payments, SubscriptionCourse
from course.validators import UrlValidator


class LessonCourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'url_video', 'course']


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field='url_video')]


class CourseSerializers(serializers.ModelSerializer):
    """Задание 3
Для сериализатора для модели курса реализуйте поле вывода уроков."""
    all_lessons = LessonCourseSerializers(many=True, read_only=True, source='lesson_set')
    number_of_lesson = serializers.SerializerMethodField()
    sub_status = serializers.SerializerMethodField()

    def get_sub_status(self, instance):
        """При этом при выборке данных по курсу пользователю необходимо присылать признак подписки текущего
        пользователя на курс. То есть давать информацию, подписан пользователь на обновления курса или нет."""
        user = self.context['request'].user.id
        obj = SubscriptionCourse.objects.filter(course=instance).filter(user=user)
        if obj:
            return obj.first().status
        return False

    def get_number_of_lesson(self, course):
        """Задание 1
Для модели курса добавьте в сериализатор поле вывода количества уроков."""
        lesson = Lesson.objects.filter(course=course)
        if lesson:
            return lesson.count()
        return 0

    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'all_lessons', 'number_of_lesson', 'sub_status', 'updated_at')


class PaymentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class SubscriptionCourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCourse
        fields = "__all__"


class PaymentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ("course",)