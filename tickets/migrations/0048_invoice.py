# Generated by Django 4.2.3 on 2023-09-04 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0047_customuser_is_analyst_customuser_is_cam_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('series', models.CharField(max_length=10)),
                ('issuance_date', models.DateField()),
                ('exit_date', models.DateField()),
                ('emitter_cnpj', models.CharField(max_length=14)),
                ('emitter_name', models.CharField(max_length=200)),
                ('recipient_cnpj', models.CharField(max_length=14)),
                ('recipient_name', models.CharField(max_length=200)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
    ]
