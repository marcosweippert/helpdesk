# Generated by Django 4.2.3 on 2023-09-11 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0050_bank_branch_drivers'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.drivers'),
        ),
    ]
