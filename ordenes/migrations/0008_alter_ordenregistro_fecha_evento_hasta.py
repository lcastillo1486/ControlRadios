# Generated by Django 4.1.5 on 2023-03-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0007_rename_fecha_evento_ordenregistro_fecha_evento_desde_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenregistro',
            name='fecha_evento_hasta',
            field=models.DateField(blank=True, null=True),
        ),
    ]
