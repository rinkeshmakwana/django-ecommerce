# Generated by Django 3.0.2 on 2020-04-08 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200408_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='default.jpg', upload_to='product_images'),
        ),
    ]
