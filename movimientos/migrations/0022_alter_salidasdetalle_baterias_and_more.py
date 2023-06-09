# Generated by Django 4.1.5 on 2023-03-10 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0021_alter_entradadetalle_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salidasdetalle',
            name='baterias',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salidasdetalle',
            name='cargadores',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salidasdetalle',
            name='cascos',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salidasdetalle',
            name='cobras',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salidasdetalle',
            name='estaciones',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salidasdetalle',
            name='handsfree',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salidasdetalle',
            name='repetidoras',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
