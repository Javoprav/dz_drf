from django.db import models
from users.models import NULLABLE, User


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='course/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)
    price = models.PositiveIntegerField(default=1000, verbose_name='стоимость курса')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='обновлен', **NULLABLE)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return f'{self.name}'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='lesson/', verbose_name='картинка', **NULLABLE)
    url_video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f'{self.name}'


class Payments(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'
    PAYMENT_TYPE = [
        (CASH, 'cash'),
        (TRANSFER, 'transfer')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_sum = models.IntegerField(verbose_name='сумма оплаты')
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=15, default=TRANSFER, verbose_name='способ оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"{self.user} - {self.payment_date}"


class SubscriptionCourse(models.Model):
    status = models.BooleanField(default=True, verbose_name='Статус подписки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

