# Generated by Django 3.2.12 on 2022-03-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fines', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fine',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='fine',
            name='student',
        ),
        migrations.AlterField(
            model_name='fine',
            name='paid_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]
