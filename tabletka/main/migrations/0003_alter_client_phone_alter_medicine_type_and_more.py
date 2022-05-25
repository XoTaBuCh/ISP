# Generated by Django 4.0.4 on 2022-05-23 21:39

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_medicine_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='type',
            field=models.CharField(choices=[('PILLS', 'PILLS'), ('CAPSULES', 'CAPSULES'), ('POWDERS', 'POWDERS'), ('SYRUP', 'SYRUP'), ('MIXTURE', 'MIXTURE'), ('OINTMENT', 'OINTMENT')], default='PILLS', max_length=10, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('IN CART', 'IN CART'), ('ACTIVE', 'ACTIVE'), ('DONE', 'DONE'), ('CANCELED', 'CANCELED'), ('DELETED', 'DELETED')], default='IN CART', max_length=10, verbose_name='Status'),
        ),
    ]
