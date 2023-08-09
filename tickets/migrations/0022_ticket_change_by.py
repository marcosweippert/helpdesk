# Generated by Django 4.2.3 on 2023-08-01 01:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0021_alter_ticket_status_alter_ticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='change_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='changed_tickets', to=settings.AUTH_USER_MODEL),
        ),
    ]
