# Generated by Django 5.0.1 on 2024-02-05 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0020_remove_detallecotizacion_cotizacion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulos',
            name='cotizacion_id',
        ),
    ]
