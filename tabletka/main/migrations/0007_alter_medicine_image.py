# Generated by Django 4.0.4 on 2022-05-28 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_medicine_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='image',
            field=models.ImageField(default='medicines/images.jpeg', upload_to='medicines', verbose_name='Image'),
        ),
    ]
