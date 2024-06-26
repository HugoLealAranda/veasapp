# Generated by Django 5.0.1 on 2024-02-05 05:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0018_articulos_preciodeventa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('nombre_empresa', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('forma_pago', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.articulos')),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionPedidos.cotizacion')),
            ],
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='articulos',
            field=models.ManyToManyField(through='gestionPedidos.DetalleCotizacion', to='gestionPedidos.articulos'),
        ),
    ]
