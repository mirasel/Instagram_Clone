# Generated by Django 3.0.8 on 2020-07-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('c', 'Custom'), ('ns', 'Prefer Not To Say')], default='ns', max_length=10),
        ),
    ]
