# Generated by Django 4.2.7 on 2024-06-01 10:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0007_alter_rating_rating_value_alter_rating_review_text'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contacts',
            new_name='ContactUs',
        ),
        migrations.AlterField(
            model_name='request',
            name='city',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabet characters are allowed!', regex='^[a-zA-Z\\s]*$')]),
        ),
        migrations.AlterField(
            model_name='request',
            name='language_spoken',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabet characters are allowed!', regex='^[a-zA-Z\\s]*$')]),
        ),
        migrations.AlterField(
            model_name='request',
            name='subjects',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only alphabet characters are allowed!', regex='^[a-zA-Z\\s]*$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Only alphabet characters are allowed!', regex='^[a-zA-Z\\s]*$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Only alphabet characters are allowed!', regex='^[a-zA-Z\\s]*$')]),
        ),
    ]