# Generated by Django 4.2.7 on 2024-05-03 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0003_alter_topic_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.TextField(max_length=50),
        ),
    ]
