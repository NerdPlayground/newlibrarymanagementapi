# Generated by Django 3.2.12 on 2022-03-09 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=255)),
                ('book_author', models.CharField(max_length=255)),
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='categories.category')),
            ],
        ),
    ]
