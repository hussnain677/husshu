# Generated by Django 3.0.8 on 2020-07-26 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200726_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('New', 'New'), ('used', 'Used')], max_length=100),
        ),
    ]
