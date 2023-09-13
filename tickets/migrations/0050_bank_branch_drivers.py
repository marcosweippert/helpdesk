# Generated by Django 4.2.3 on 2023-09-06 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0049_alter_invoice_recipient_cnpj_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('website', models.URLField(blank=True)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.bank')),
            ],
        ),
        migrations.CreateModel(
            name='Drivers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('cnpj', models.CharField(max_length=18, unique=True)),
                ('account_type', models.CharField(choices=[('Checking', 'Checking'), ('Savings', 'Savings')], max_length=10)),
                ('account_number', models.CharField(max_length=20)),
                ('account_digit', models.CharField(max_length=2)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.bank')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.branch')),
            ],
        ),
    ]
