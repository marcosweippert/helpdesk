# Generated by Django 4.2.3 on 2023-08-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0046_workorder_complete_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_analyst',
            field=models.BooleanField(default=False, verbose_name='Analyst'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_cam',
            field=models.BooleanField(default=False, verbose_name='CAM'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_manager',
            field=models.BooleanField(default=False, verbose_name='Manager'),
        ),
    ]
