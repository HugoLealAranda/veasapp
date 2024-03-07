from django.contrib import admin
from gestionPedidos import views
from gestionPedidos.views import cotizacion_view
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', views.buscar, name='buscar'),
    path('home/', views.home, name='home'), 
    path('', views.home, name='home'),
    path('ruta/cotizacion/', cotizacion_view, name='agregar_cotizacion'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('send_message/', views.send_message, name='send_message'),
    path('lista_tareas/', views.lista_tareas, name='lista_tareas'),  # Si deseas mantener esta ruta

]

