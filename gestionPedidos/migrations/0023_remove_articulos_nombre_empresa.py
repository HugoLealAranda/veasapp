# Generated by Django 5.0.1 on 2024-02-06 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0022_remove_articulos_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulos',
            name='nombre_empresa',
        ),
    ]
