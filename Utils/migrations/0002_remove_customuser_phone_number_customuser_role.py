# Generated by Django 5.1.7 on 2025-03-22 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utils', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('staff', 'Staff')], default='staff', max_length=10),
        ),
    ]
