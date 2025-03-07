# Generated by Django 5.1.7 on 2025-03-08 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
