# Generated by Django 4.2.1 on 2023-05-24 17:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carseller', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caruser',
            name='fav_cars',
            field=models.ManyToManyField(to='carseller.car'),
        ),
        migrations.AddField(
            model_name='caruser',
            name='fav_sellers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]