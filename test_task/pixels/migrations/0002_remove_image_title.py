# Generated by Django 3.2.4 on 2021-09-17 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pixels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
    ]