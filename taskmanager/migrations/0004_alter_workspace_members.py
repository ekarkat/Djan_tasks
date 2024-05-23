# Generated by Django 5.0.6 on 2024-05-23 20:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0003_alter_workspace_members'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='shared_workspaces', to=settings.AUTH_USER_MODEL),
        ),
    ]
