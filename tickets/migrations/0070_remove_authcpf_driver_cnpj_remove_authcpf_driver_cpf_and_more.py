# Generated by Django 4.2.3 on 2023-09-13 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0069_rename_bank_id_customuser_bank_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authcpf',
            name='driver_cnpj',
        ),
        migrations.RemoveField(
            model_name='authcpf',
            name='driver_cpf',
        ),
        migrations.AddField(
            model_name='authcpf',
            name='cnpj',
            field=models.CharField(blank=True, max_length=18, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='authcpf',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
    ]
