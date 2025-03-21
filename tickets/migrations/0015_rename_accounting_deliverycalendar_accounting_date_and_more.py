# Generated by Django 4.2.3 on 2023-07-30 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0014_deliverycalendar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='accounting',
            new_name='accounting_date',
        ),
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='approval',
            new_name='approval_date',
        ),
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='changes',
            new_name='changes_date',
        ),
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='esocial_delivery',
            new_name='esocial_delivery_date',
        ),
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='net_salaries',
            new_name='net_salaries_date',
        ),
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='next_month_vacations',
            new_name='next_month_vacations_date',
        ),
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='payroll_preview',
            new_name='payroll_preview_date',
        ),
        migrations.RenameField(
            model_name='deliverycalendar',
            old_name='taxes',
            new_name='taxes_date',
        ),
    ]
