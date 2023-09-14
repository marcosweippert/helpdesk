# Generated by Django 4.2.3 on 2023-09-13 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0073_alter_invoice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Finance Approval', 'Finance Approval'), ('Paid', 'Paid'), ('Driver Check', 'Driver Check')], default='Pending', max_length=20),
        ),
    ]
