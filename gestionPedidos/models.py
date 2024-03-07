from django.db import models
from django.contrib.auth.models import User


class Articulos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Artículo")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    unidad = models.CharField(max_length=20, verbose_name="Unidad")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitario")
    fecha = models.DateField(verbose_name="Fecha", null=True, blank=True)
    lugar = models.CharField(max_length=100, verbose_name="Lugar", null=True, blank=True)
    vendedor = models.CharField(max_length=100, verbose_name="Vendedor", null=True, blank=True)
    comprador = models.CharField(max_length=100, verbose_name="Comprador", null=True, blank=True)
    empresa_compradora = models.CharField(max_length=100, verbose_name="Empresa Compradora", null=True, blank=True)
    empresa_vendedora = models.CharField(max_length=100, verbose_name="Empresa Vendedora", null=True, blank=True)
    forma_pago = models.CharField(max_length=100, verbose_name="Forma de Pago", null=True, blank=True)
    entrega = models.CharField(max_length=100, verbose_name="Entrega", null=True, blank=True)
    correo_vendedor = models.EmailField(verbose_name="Correo del Vendedor", null=True, blank=True)
    numero_factura = models.CharField(max_length=100, verbose_name="Número de Factura", null=True, blank=True)
    numero_boleta = models.CharField(max_length=100, verbose_name="Número de Boleta", null=True, blank=True)
    numero_cotizacion = models.CharField(max_length=100, verbose_name="Número de Cotización", null=True, blank=True)
    seccion = models.CharField(max_length=100, verbose_name="Sección", null=True, blank=True)
    comentarios = models.TextField(verbose_name="Comentarios", null=True, blank=True)
    aprobado = models.CharField(max_length=20, verbose_name="Aprobado/Rechazado", choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre}"

    @property
    def valor_total(self):
        return self.cantidad * self.valor_unitario

    class Meta:
        verbose_name = "Articulos"
        verbose_name_plural = "Articulos"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(null=True)  # Cambio realizado aquí
    fecha_vencimiento = models.DateField()
    completada = models.BooleanField(default=False)
    asignadas = models.ManyToManyField(User, related_name='tareas_asignadas', blank=True)

    def __str__(self):
        return self.titulo
