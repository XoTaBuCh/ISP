# Generated by Django 4.0.4 on 2022-05-28 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_medicine_max_price_remove_medicine_min_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='image',
            field=models.ImageField(upload_to='medicines', verbose_name='Image'),
        ),
    ]
