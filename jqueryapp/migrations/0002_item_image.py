# Generated by Django 3.0.2 on 2020-01-29 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jqueryapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='item'),
        ),
    ]