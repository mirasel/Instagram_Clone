# Generated by Django 3.1 on 2020-08-06 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='title',
            field=models.TextField(blank=True, max_length=60),
        ),
    ]