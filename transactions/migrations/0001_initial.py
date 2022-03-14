# Generated by Django 3.2.12 on 2022-03-14 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued', models.BooleanField(default=False)),
                ('issued_at', models.DateTimeField(blank=True, null=True)),
                ('returned', models.BooleanField(default=False)),
                ('returned_at', models.DateTimeField(blank=True, null=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction', to='books.book')),
                ('issued_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', to='students.student')),
            ],
        ),
    ]
