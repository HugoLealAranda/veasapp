from django.contrib import admin
from gestionPedidos.models import Articulos
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Tarea
from .models import Message




class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'fecha_vencimiento', 'completada')
    list_filter = ('completada',)
    search_fields = ('titulo', 'descripcion')
    list_editable = ('completada',)
    actions = ['marcar_como_completada']

    def marcar_como_completada(self, request, queryset):
        queryset.update(completada=True)
        self.message_user(request, "Las tareas seleccionadas se han marcado como completadas.")

    marcar_como_completada.short_description = "Marcar como completadas"

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

def renombrar_rental_veas(modeladmin, request, queryset):
    queryset.update(empresa_compradora='rental veas')
    modeladmin.message_user(request, "El campo 'empresa_compradora' se ha renombrado a 'rental veas' en los artículos seleccionados.")

def renombrar_empresa_vendedora(modeladmin, request, queryset):
    queryset.update(empresa_vendedora='rental veas')
    modeladmin.message_user(request, "El campo 'empresa_vendedora' se ha renombrado a 'Rental Veas' en los artículos seleccionados.")

def aprobar_documento(modeladmin, request, queryset):
    queryset.update(aprobado='aprobado')
    modeladmin.message_user(request, "se han aprobado los articulos seleccionados")

def rechazar_documento(modeladmin, request, queryset):
    queryset.update(aprobado='rechazado')
    modeladmin.message_user(request, "se han rechazado los articulos seleccionados")

renombrar_empresa_vendedora.short_description = "Renombrar empresa vendedora a Rental Veas"
renombrar_rental_veas.short_description = "Renombrar empresa compradora a Rental Veas"
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
        'lugar', 
        'vendedor',  
        'comprador',  
        'unidad',  
        'numero_factura',  
        'numero_cotizacion',  
        'numero_boleta',  
        CotizacionFilter, 
    )
    actions = [
        cambiar_seccion_a_ferreteria,
        cambiar_seccion_a_electricidad,
        cambiar_seccion_a_pintura,
        cambiar_seccion_a_muebles,
        cambiar_seccion_a_maestranza,
        cambiar_seccion_a_mineria,
        renombrar_rental_veas,
        renombrar_empresa_vendedora,
        aprobar_documento,
        rechazar_documento,

    ]

    list_per_page = 20
    list_filter_collapse = True


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    search_fields = ('content',)
    list_filter = ('user', 'timestamp')



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
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Message, MessageAdmin)
