# Generated by Django 2.0.1 on 2018-02-21 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_credential'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='password',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='credential',
            name='username',
            field=models.CharField(max_length=200),
        ),
    ]
