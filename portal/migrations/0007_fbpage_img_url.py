# Generated by Django 2.0.2 on 2018-03-16 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_fbpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbpage',
            name='img_url',
            field=models.CharField(default='to_be_changed', max_length=100),
        ),
    ]
