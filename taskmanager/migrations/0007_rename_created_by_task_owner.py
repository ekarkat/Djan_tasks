# Generated by Django 5.0.6 on 2024-05-23 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0006_alter_unit_members_alter_unit_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='created_by',
            new_name='owner',
        ),
    ]
