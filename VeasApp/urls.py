from django.contrib import admin
from gestionPedidos import views
from gestionPedidos.views import cotizacion_view
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', views.buscar, name='buscar'),
    path('home/', views.home, name='home_view'), 
    path('', views.home_view, name='home'),
    path('ruta/cotizacion/', cotizacion_view, name='agregar_cotizacion'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Usar el nombre de la URL, no el archivo de plantilla
    path('login/', auth_views.LoginView.as_view(), name='login'),

]

