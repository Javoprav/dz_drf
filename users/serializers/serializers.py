from rest_framework import serializers
from course.models import Payments
from users.models import User


class UserPaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UsersSerializers(serializers.ModelSerializer):
    """* Дополнительное задание
Для профиля пользователя сделайте вывод истории платежей, расширив сериализатор для вывода списка платежей."""
    all_payments = UserPaymentSerializers(many=True, read_only=True, source='payments_set')
#     number_of_lesson = serializers.SerializerMethodField()
#
#     def get_number_of_lesson(self, course):
#         """Задание 1
# Для модели курса добавьте в сериализатор поле вывода количества уроков."""
#         lesson = Lesson.objects.filter(course=course)
#         if lesson:
#             return lesson.count()
#         return 0

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'all_payments', 'role')


class ForAuthUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city')


class ForCreateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
