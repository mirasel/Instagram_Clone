# Generated by Django 3.1 on 2020-08-06 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200806_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='title',
            field=models.TextField(blank=True, max_length=50),
        ),
    ]
