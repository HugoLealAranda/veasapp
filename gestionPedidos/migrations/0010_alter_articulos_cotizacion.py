# Generated by Django 5.0.1 on 2024-02-04 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0009_alter_articulos_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='cotizacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='gestionPedidos.detallecotizacion'),
        ),
    ]
