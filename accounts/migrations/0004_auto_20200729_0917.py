# Generated by Django 3.0.8 on 2020-07-29 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200728_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('ns', 'Prefer Not To Say')], default='ns', max_length=2),
        ),
    ]
