# Generated by Django 4.2.3 on 2023-07-29 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticket_attachment_ticket_department_ticket_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='partner',
            field=models.CharField(max_length=100),
        ),
    ]
