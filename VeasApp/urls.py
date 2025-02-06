from django.contrib import admin
from gestionPedidos import views
from gestionPedidos.views import cotizacion_view
from django.urls import path, include
from django.contrib.auth import views as auth_views
from gestionPedidos.views import generar_informe
from gestionPedidos.views import buscar_articulos_nombres



urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', views.buscar, name='buscar'),
    path('home/', views.home, name='home'),
    path('productos_agregados_correctamente/', views.productos_agregados_correctamente, name='productos_agregados_correctamente'),
    path('', views.home, name='home'),
    path('ruta/cotizacion/', cotizacion_view, name='agregar_cotizacion'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('send_message/', views.send_message, name='send_message'),
    path('lista_tareas/', views.lista_tareas, name='lista_tareas'),  # Si deseas mantener esta ruta
    path('generar_informe/', generar_informe, name='generar_informe'),
    path('buscar_articulos_nombres/', buscar_articulos_nombres, name='buscar_articulos_nombres'),
    path('buscar_lugares/', views.buscar_lugares, name='buscar_lugares'),
    path('buscar_vendedores/', views.buscar_vendedores, name='buscar_vendedores'),
    path('buscar_compradores/', views.buscar_compradores, name='buscar_compradores'),
    path('buscar_empresas_compradoras/', views.buscar_empresas_compradoras, name='buscar_empresas_compradoras'),
    path('buscar_empresas_vendedoras/', views.buscar_empresas_vendedoras, name='buscar_empresas_vendedoras'),
    path('buscar_formas_pago/', views.buscar_formas_pago, name='buscar_formas_pago'),
    path('buscar_entregas/', views.buscar_entregas, name='buscar_entregas'),
    path('buscar_secciones/', views.buscar_secciones, name='buscar_secciones'),
    path('buscar_correos_vendedor/', views.buscar_correos_vendedor, name='buscar_correos_vendedor'),
    #path('informe-mensual/', informe_mensual, name='informe_mensual'),
    #path('informe-semestral/', informe_semestral, name='informe_semestral'),
    #path('informe-anual/', informe_anual, name='informe_anual'),
]

