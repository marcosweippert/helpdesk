# Generated by Django 4.2.3 on 2023-09-12 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0056_customuser_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='account_digit',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='account_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='account_type',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='cnpj',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='cpf',
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('cnpj', models.CharField(blank=True, max_length=18, null=True, unique=True)),
                ('account_type', models.CharField(blank=True, choices=[('Checking', 'Checking'), ('Savings', 'Savings')], max_length=10, null=True)),
                ('account_number', models.CharField(blank=True, max_length=20, null=True)),
                ('account_digit', models.CharField(blank=True, max_length=2, null=True)),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.bank')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.branch')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
