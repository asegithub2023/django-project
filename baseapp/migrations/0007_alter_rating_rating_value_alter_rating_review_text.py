# Generated by Django 4.2.7 on 2024-05-18 05:53

import baseapp.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0006_rating_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating_value',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='rating',
            name='review_text',
            field=models.TextField(validators=[baseapp.models.validate_review_text]),
        ),
    ]
