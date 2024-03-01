from django.contrib import admin
from gestionPedidos.models import Articulos
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


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


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.register(Articulos, ArticulosAdmin)
custom_admin_site = CustomAdminSite(name='custom_admin')
admin.site = custom_admin_site
custom_admin_site.register(Articulos, ArticulosAdmin)
admin.site.register(User, CustomUserAdmin)