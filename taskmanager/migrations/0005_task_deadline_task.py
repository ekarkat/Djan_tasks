# Generated by Django 5.0.6 on 2024-06-05 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0004_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline_task',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]