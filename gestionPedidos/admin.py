from django.contrib import admin
from gestionPedidos.models import Articulos
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.utils.translation import ngettext


class CustomAdminSite(AdminSite):
    site_header = 'Administracion Veas App'

class ClientesAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "telefono")
    search_fields = ("nombre", "telefono", "direccion")
    list_filter = ("direccion",)

class CotizacionFilter(admin.SimpleListFilter):
    title = 'Cotizaciones'
    parameter_name = 'cotizaciones'

    def lookups(self, request, model_admin):
        return (
            ('aprobadas', 'Aprobadas'),
            ('rechazadas', 'Rechazadas'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'aprobadas':
            return queryset.filter(aprobado='aprobado', numero_cotizacion__isnull=False)
        if self.value() == 'rechazadas':
            return queryset.filter(aprobado='rechazado', numero_cotizacion__isnull=False)

def cambiar_seccion_a_ferreteria(admin, request, queryset):
    queryset.update(seccion='ferreteria')

def cambiar_seccion_a_electricidad(admin, request, queryset):
    queryset.update(seccion='electricidad')

def cambiar_seccion_a_pintura(admin, request, queryset):
    queryset.update(seccion='pintura')

def cambiar_seccion_a_maestranza(admin, request, queryset):
    queryset.update(seccion='maestranza')

def cambiar_seccion_a_muebles(admin, request, queryset):
    queryset.update(seccion='muebles')

def cambiar_seccion_a_mineria(admin, request, queryset):
    queryset.update(seccion='mineria')


class ArticulosAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'cantidad', 'unidad', 'valor_unitario', 'fecha', 'lugar', 'vendedor', 'comprador',
        'empresa_compradora', 'empresa_vendedora', 'forma_pago', 'entrega', 'correo_vendedor',
        'numero_factura', 'numero_boleta', 'numero_cotizacion', 'seccion', 'comentarios', 'aprobado'
    )
    search_fields = ['nombre', 'vendedor', 'comprador', 'empresa_compradora', 'empresa_vendedora', 'numero_factura', 'numero_cotizacion', 'numero_boleta']
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
        'numero_boleta',  # Filtro para número de boleta insensible a mayúsculas y minúsculas
        CotizacionFilter,  # Filtro combinado para cotizaciones aprobadas/rechazadas con número de cotización no nulo
    )
    actions = [
        cambiar_seccion_a_ferreteria,
        cambiar_seccion_a_electricidad,
        cambiar_seccion_a_pintura,
        cambiar_seccion_a_muebles,
        cambiar_seccion_a_maestranza,
        cambiar_seccion_a_mineria,
    ]







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