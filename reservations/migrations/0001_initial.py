# Generated by Django 3.2.12 on 2022-03-24 13:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book_items', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reserved_on', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=255)),
                ('book_item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reservations', to='book_items.bookitem')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='students.student')),
            ],
        ),
    ]
