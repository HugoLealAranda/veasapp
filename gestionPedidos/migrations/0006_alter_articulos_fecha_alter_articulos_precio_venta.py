# Generated by Django 5.0.1 on 2024-02-04 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0005_alter_articulos_cotizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='fecha',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='articulos',
            name='precio_venta',
            field=models.IntegerField(null=True),
        ),
    ]
