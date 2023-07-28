from django.conf import settings
from django.core.mail import send_mail

from course.models import SubscriptionCourse, Course
from datetime import datetime, timedelta
from celery import shared_task

from users.models import User


@shared_task
def send_mail_user_update(object_pk):
    """Добавьте асинхронную рассылку писем пользователям об обновлении материалов курса."""
    """Пользователь может обновлять каждый урок курса отдельно. Добавьте проверку на то, что уведомление отправляется
        только в том случае, если курс не обновлялся более 4 часов."""
    subs_list = SubscriptionCourse.objects.filter(course=object_pk)
    # current_time = datetime.now()
    # last_updated_time = Course.objects.get(id=object_pk).updated_at
    # time_difference = current_time - last_updated_time
    # if time_difference > timedelta(hours=4):
    for item in subs_list:
        print(item.user)
        print(f"Send mail for user in {item}")
        send_mail(
            subject='Обновление',
            message=f'Обновление курса(ов) {subs_list}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[item.user.email]
        )


def check_user():
    """С помощью celery-beat реализуйте фоновую задачу, которая будет проверять пользователей по дате последнего
    входа по полю last_login и, если пользователь не заходил более месяца, блокировать его с помощью флага is_active """
    user_list = User.objects.all()
    for user in user_list:
        if user.last_login > datetime.now() - timedelta(days=30):
            user.is_active = False
            user.save()