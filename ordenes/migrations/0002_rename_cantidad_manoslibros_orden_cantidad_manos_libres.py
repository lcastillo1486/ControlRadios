# Generated by Django 4.1.5 on 2023-01-26 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orden',
            old_name='cantidad_manoslibros',
            new_name='cantidad_manos_libres',
        ),
    ]
