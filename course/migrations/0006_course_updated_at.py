# Generated by Django 4.2.3 on 2023-07-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_price_alter_course_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='обновлен'),
        ),
    ]
