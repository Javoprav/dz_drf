import stripe
from django.conf import settings
import requests
from course.models import Payments


def checkout_session(course, user):
    # session = stripe.checkout.Session.create(
    #         payment_method_types=['card'],
    #         line_items=[
    #             {'price_data': {
    #                     'currency': 'usd',
    #                     'unit_amount': course.price,
    #                     'product_data': {
    #                         'name': course
    #                     }
    #                 },
    #                 'quantity': 1}],
    #         mode='payment',
    #         success_url=settings.DOMAIN + '/success/',
    #         cancel_url=settings.DOMAIN + '/cancel/',)
    """Да, все верно, он возвращает id сессии...

Ты можешь потом сделать get-запрос на
GET /v1/checkout/sessions/<session_id>
и получишь id платежа в поле payment_intent, причем если платеж не был осуществлен (не путать с ошибкой), то сессия будет считаться протухшей, в в поле payment_intent будет стоять null

По нему можно получить сам платеж, где указан статус
GET /v1/payment_intents/<payment_id>"""

    # session = stripe.PaymentIntent.create(
    #     amount=course.price,
    #     currency="usd",
    #     automatic_payment_methods={"enabled": True},
    # )
    # return session

    headers = {'Authorization': f'Bearer {settings.STRIPE_SECRET_KEY}'}
    data = [
        ('amount', course.price),
        ('currency', 'usd'),
    ]
    response = requests.post(f'{settings.STRIPE_URL}/payment_intents', headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f'ошибка : {response.json()["error"]["message"]}')
    return response.json()


def create_payment(course, user):
    Payments.objects.create(
        user=user,
        course=course,
        payment_sum=course.price,
    )
