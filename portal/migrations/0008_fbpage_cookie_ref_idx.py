# Generated by Django 2.0.2 on 2018-03-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_fbpage_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbpage',
            name='cookie_ref_idx',
            field=models.CharField(default='0', max_length=3),
        ),
    ]
