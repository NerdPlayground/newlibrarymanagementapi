# Generated by Django 3.2.12 on 2022-03-17 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('racks', '0001_initial'),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=255)),
                ('purchased_on', models.DateField()),
                ('published_on', models.DateField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_items', to='books.book')),
                ('rack', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='book_items', to='racks.rack')),
            ],
        ),
    ]
