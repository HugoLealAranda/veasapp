# Generated by Django 5.0.1 on 2024-02-04 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0010_alter_articulos_cotizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='cotizacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='gestionPedidos.detallecotizacion'),
        ),
    ]
