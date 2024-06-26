# Generated by Django 5.0.1 on 2024-02-05 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPedidos', '0019_cotizacion_detallecotizacion_cotizacion_articulos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallecotizacion',
            name='cotizacion',
        ),
        migrations.RemoveField(
            model_name='detallecotizacion',
            name='articulo',
        ),
        migrations.AlterModelOptions(
            name='articulos',
            options={'verbose_name': 'Articulos', 'verbose_name_plural': 'Articulos'},
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='contacto',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='precio',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='preciodeventa',
        ),
        migrations.AddField(
            model_name='articulos',
            name='cantidad',
            field=models.IntegerField(default=1, verbose_name='Cantidad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articulos',
            name='comprador',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Comprador'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='correo_vendedor',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo del Vendedor'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='cotizacion_id',
            field=models.CharField(default=1, max_length=100, verbose_name='ID de Cotización'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articulos',
            name='descripcion',
            field=models.CharField(default=1, max_length=255, verbose_name='Descripción'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articulos',
            name='empresa_compradora',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Empresa Compradora'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='empresa_vendedora',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Empresa Vendedora'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='entrega',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Entrega'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='forma_pago',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Forma de Pago'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='nombre_empresa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre Empresa'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='numero_cotizacion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número de Cotización'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='numero_factura',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número de Factura'),
        ),
        migrations.AddField(
            model_name='articulos',
            name='unidad',
            field=models.CharField(default=1, max_length=20, verbose_name='Unidad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articulos',
            name='valor_unitario',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Valor Unitario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articulos',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='articulos',
            name='lugar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Lugar'),
        ),
        migrations.AlterField(
            model_name='articulos',
            name='nombre',
            field=models.CharField(max_length=255, verbose_name='Nombre del Artículo'),
        ),
        migrations.AlterField(
            model_name='articulos',
            name='seccion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Sección'),
        ),
        migrations.AlterField(
            model_name='articulos',
            name='vendedor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Vendedor'),
        ),
        migrations.DeleteModel(
            name='Cotizacion',
        ),
        migrations.DeleteModel(
            name='DetalleCotizacion',
        ),
    ]
