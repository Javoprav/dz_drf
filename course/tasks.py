from celery import shared_task
from course.models import SubscriptionCourse


@shared_task
def send_mail_user_update(object):
    """Добавьте асинхронную рассылку писем пользователям об обновлении материалов курса."""
    subs_list = SubscriptionCourse.objects.filter(course=object)
    for item in subs_list:
        print(item)
        print(f"Send mail for user in {item}")

