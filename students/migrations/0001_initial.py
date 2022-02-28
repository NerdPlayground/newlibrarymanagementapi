# Generated by Django 4.0.2 on 2022-02-27 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('registration_number', models.CharField(blank=True, max_length=8, unique=True)),
                ('campus', models.CharField(blank=True, max_length=255)),
                ('faculty', models.CharField(blank=True, max_length=255)),
                ('course', models.CharField(blank=True, max_length=255)),
                ('mode_of_study', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]