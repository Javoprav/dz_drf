import stripe
from django.conf import settings

from course.models import Payments


def checkout_session(course):
    session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {'price_data': {
                        'currency': 'usd',
                        'unit_amount': course.price,
                        'product_data': {
                            'name': course
                        }
                    },
                    'quantity': 1}],
            mode='payment',
            success_url=settings.DOMAIN + '/success/',
            cancel_url=settings.DOMAIN + '/cancel/',)
    return session


def create_payment(course, user):
    Payments.objects.create(
        user=user,
        course=course,
        payment_sum=course.price,
    )
