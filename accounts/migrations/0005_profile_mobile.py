# Generated by Django 3.0.8 on 2020-07-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200729_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobile',
            field=models.IntegerField(default=0),
        ),
    ]
