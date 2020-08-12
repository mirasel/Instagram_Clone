# Generated by Django 3.1 on 2020-08-12 09:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_delete_postlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date Published'),
            preserve_default=False,
        ),
    ]
