# Generated by Django 5.0.1 on 2024-02-05 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0017_remove_articulos_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulos',
            name='preciodeventa',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
