# Generated by Django 3.0.8 on 2020-07-27 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200727_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='user/default.png', upload_to='user/'),
        ),
    ]
