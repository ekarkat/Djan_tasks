# Generated by Django 5.0.6 on 2024-06-06 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0005_task_deadline_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='deadline_task',
        ),
    ]