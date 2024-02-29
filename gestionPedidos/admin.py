from django.contrib import admin
from gestionPedidos.models import Articulos
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'Administracion Veas App'

class ClientesAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "telefono")
    search_fields = ("nombre", "telefono", "direccion")
    list_filter = ("direccion",)

class ArticulosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'unidad', 'valor_unitario', 'fecha', 'lugar', 'vendedor', 'comprador', 'empresa_compradora', 'empresa_vendedora', 'forma_pago', 'entrega', 'correo_vendedor', 'numero_factura', 'numero_cotizacion', 'seccion')
    search_fields = ['nombre', 'vendedor', 'comprador', 'empresa_compradora', 'empresa_vendedora', 'numero_factura', 'numero_cotizacion']
    list_filter = (
        'seccion',
        'empresa_compradora',
        'empresa_vendedora',
        'fecha',
        'entrega',
        'forma_pago',
        'lugar',  # Filtro para lugar insensible a mayúsculas y minúsculas
        'vendedor',  # Filtro para vendedor insensible a mayúsculas y minúsculas
        'comprador',  # Filtro para comprador insensible a mayúsculas y minúsculas
        'unidad',  # Filtro para unidad insensible a mayúsculas y minúsculas
        'numero_factura',  # Filtro para número de factura insensible a mayúsculas y minúsculas
        'numero_cotizacion',  # Filtro para número de cotización insensible a mayúsculas y minúsculas
    )





admin.site.register(Articulos, ArticulosAdmin)
custom_admin_site = CustomAdminSite(name='custom_admin')
admin.site = custom_admin_site
custom_admin_site.register(Articulos, ArticulosAdmin)
