from django.http import HttpResponse
from django.shortcuts import render, redirect
from collections import Counter
from .models import Articulos
from django.forms import formset_factory
from django.db.models import Avg
import matplotlib
matplotlib.use('Agg')
from django.db.models import Min, Max
import json
from django.db.models import Count
from django.db.models.functions import Round
from .forms import CotizacionForm
from .forms import ArticuloCotizacionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum, F, FloatField
from gestionPedidos.models import Message
from django.contrib.auth.decorators import login_required
from .models import Tarea
from django.db.models import F, Sum
from django.db.models import Sum
from django.db.models import Q




@login_required
def lista_tareas(request):
    usuario_actual = request.user
    tareas_pendientes = Tarea.objects.filter(completada=False).order_by('-fecha_creacion')[:5]
    tareas_completadas = Tarea.objects.filter(completada=True).order_by('-fecha_creacion')[:5]
    return render(request, 'home.html', {'tareas_pendientes': tareas_pendientes, 'tareas_completadas': tareas_completadas})


@login_required
def chat_room(request):
    messages = Message.objects.all()
    return render(request, 'home.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
    return redirect('home')



def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'


    return response


@login_required
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirecciona a una página después del login exitoso
            return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'registration/login.html')


from .models import Message

@login_required
def home(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
            return redirect('home')  # Redirecciona después de enviar un mensaje

    # Obtener los últimos 10 mensajes ordenados por fecha de creación
    messages = Message.objects.order_by('-timestamp')[:15]

    # Obtener solo las últimas 5 tareas pendientes y completadas
    tareas_pendientes = Tarea.objects.filter(completada=False).order_by('-fecha_creacion')[:5]
    tareas_completadas = Tarea.objects.filter(completada=True).order_by('-fecha_creacion')[:5]

    # Modificar los nombres de usuario para que solo contengan la parte antes del '@'
    for tarea in tareas_pendientes:
        tarea.nombres_asignados = ", ".join([asignado.username.split("@")[0] for asignado in tarea.asignadas.all()])
    for tarea in tareas_completadas:
        tarea.nombres_asignados = ", ".join([asignado.username.split("@")[0] for asignado in tarea.asignadas.all()])

    return render(request, 'home.html', {'messages': messages, 'tareas_pendientes': tareas_pendientes, 'tareas_completadas': tareas_completadas})








@login_required
def busqueda_productos(request):
    
    return render(request, "busqueda_productos.html")



@login_required
def buscar(request):
    if 'prd' in request.GET and request.GET['prd']:
        producto = request.GET['prd']  
        if len(producto) > 100:
            return HttpResponse("Texto de búsqueda demasiado largo")
        else:
            articulos = Articulos.objects.filter(nombre__icontains=producto).order_by('fecha')
            if articulos.exists():
                

                
                empresas_valores = articulos.exclude(empresa_vendedora__iexact='Rental Veas') \
                                            .values('empresa_vendedora') \
                                            .annotate(valor_unitario_min=Min('valor_unitario')) \

                ultimo_articulo_otros = articulos.exclude(empresa_vendedora__iexact='Rental Veas').order_by('-fecha').first()


                ultimo_valor_otros = ultimo_articulo_otros.valor_unitario if ultimo_articulo_otros else 0


                promedio_rental_veas = articulos.filter(
                    empresa_vendedora__iexact='Rental Veas'
                ).aggregate(
                    promedio_rental_veas=Round(Avg('valor_unitario'), 2)
                )['promedio_rental_veas']




                promedio_otros = articulos.exclude(empresa_vendedora__iexact='Rental Veas') \
                                .aggregate(promedio_otros=Round(Avg('valor_unitario'), 2))['promedio_otros']



                empresas_con_producto = Articulos.objects.filter(
                    nombre__icontains=producto
                ).values('empresa_vendedora').distinct()






                transacciones_recientes = Articulos.objects.filter(
                    empresa_vendedora__in=empresas_con_producto
                ).exclude(entrega__isnull=True).values(
                    'empresa_vendedora'
                ).annotate(
                    ultima_transaccion=Max('fecha')
                )

                # Obtener los detalles de la transacción más reciente para cada empresa vendedora
                resultados = []
                for transaccion in transacciones_recientes:
                    empresa = transaccion['empresa_vendedora']
                    transaccion_mas_reciente = Articulos.objects.filter(
                        empresa_vendedora=empresa,
                        fecha=transaccion['ultima_transaccion'],
                        entrega__isnull=False,  # Asegurar que la entrega no sea nula
                        nombre__icontains=producto  # Verificar si la transacción es para el artículo buscado
                    ).first()
                    if transaccion_mas_reciente:
                        resultados.append({
                            'empresa_vendedora': empresa,
                            'entrega': transaccion_mas_reciente.entrega
                        })






                volumen_ventas_por_empresa = Articulos.objects.exclude(empresa_vendedora__iexact='Rental Veas') \
                                            .exclude(numero_cotizacion__isnull=True) \
                                            .filter(nombre__icontains=producto) \
                                            .values('empresa_vendedora') \
                                            .annotate(volumen_total=Sum('cantidad')) \
                                            .order_by('-volumen_total')



                valor_ventas_por_empresa = articulos.exclude(empresa_vendedora__iexact='Rental Veas') \
                                                    .exclude(numero_cotizacion__isnull=True) \
                                                    .annotate(valor_total=F('cantidad') * F('valor_unitario')) \
                                                    .values('empresa_vendedora') \
                                                    .annotate(valor_total_sum=Sum('valor_total', output_field=FloatField())) \
                                                    .order_by('-valor_total_sum')




                rendimiento_compradores = articulos.exclude(numero_cotizacion__isnull=True) \
                                                    .filter(nombre__icontains=producto) \
                                                    .values('comprador') \
                                                    .annotate(total_comprado=Sum('cantidad'), 
                                                            valor_total_comprado=Sum(F('cantidad') * F('valor_unitario'))) \
                                                    .order_by('-total_comprado')
                
                compras_totales_veas = Articulos.objects.exclude(empresa_vendedora__iexact='Rental Veas') \
                                                        .exclude(numero_cotizacion__isnull=True) \
                                                        .filter(nombre__icontains=producto) \
                                                        .values('empresa_vendedora') \
                                                        .annotate(volumen_total=Sum('cantidad')) \
                                                        .order_by('-volumen_total') 
                
                ventas_totales_veas = Articulos.objects.filter(empresa_vendedora__iexact='Rental Veas') \
                                                        .exclude(numero_cotizacion__isnull=True) \
                                                        .filter(nombre__icontains=producto) \
                                                        .values('empresa_vendedora') \
                                                        .annotate(volumen_total=Sum('cantidad')) \
                                                        .order_by('-volumen_total')


                total_compras_veas = sum(item['volumen_total'] for item in compras_totales_veas)

                
                total_ventas_veas = sum(item['volumen_total'] for item in ventas_totales_veas)



                stock_teorico=total_compras_veas-total_ventas_veas



                ultimo_valor_rental_veas = articulos.filter(empresa_vendedora__iexact='Rental Veas').order_by('-fecha').first().valor_unitario if articulos.filter(empresa_vendedora__iexact='Rental Veas').exists() else 0
                

                
                
                ultimo_articulo_otros = articulos.exclude(empresa_vendedora__iexact='Rental Veas').order_by('-fecha').first()
                


                
                ultimo_valor_otros = ultimo_articulo_otros.valor_unitario if ultimo_articulo_otros else 0
                utilidad = ultimo_valor_rental_veas - ultimo_valor_otros if ultimo_valor_rental_veas and ultimo_valor_otros else 0      
                utilidad_porcentual = (utilidad / ultimo_valor_otros * 100) if ultimo_valor_otros else 0
                
                
                
                
                
                metricas1 = {
                    'ultimo_valor_rental_veas': ultimo_valor_rental_veas,
                    'ultimo_valor_otros': ultimo_valor_otros,
                    'promedio_rental_veas': promedio_rental_veas,
                    'promedio_otros': promedio_otros,
                    'rendimiento_compradores': rendimiento_compradores,
                    'utilidad': utilidad,
                    'utilidad_porcentual': utilidad_porcentual,
                             }
                



                metricas2 = {
                    'valor_ventas_por_empresa': valor_ventas_por_empresa,            
                             }
                
                metricas4 = {
                    'volumen_ventas_por_empresa': volumen_ventas_por_empresa,
                             }
                

                metricas3 = {
                    'rendimiento_compradores': rendimiento_compradores,
                             }
                

                

                #preparar los datos para el grafico de lineas
                fechas_rental_veas = []
                valores_unitarios_rental_veas = []
                articulos_rental_veas = articulos.filter(empresa_vendedora='Rental Veas').exclude(fecha__isnull=True)

                if articulos_rental_veas:
                    fechas_rental_veas = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_rental_veas]
                    valores_unitarios_rental_veas = [float(articulo.valor_unitario) for articulo in articulos_rental_veas] 
                fechas_otros = []
                valores_unitarios_otros = []
                articulos_otros = articulos.exclude(empresa_vendedora='Rental Veas').exclude(fecha__isnull=True)

                if articulos_otros:
                    fechas_otros = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_otros]
                    valores_unitarios_otros = [float(articulo.valor_unitario) for articulo in articulos_otros] 
            


                # Preparar los datos para el gráfico de torta
                lugares = [articulo.lugar for articulo in articulos if articulo.lugar]
                conteo_lugares = Counter(lugares)
                etiquetas_pie = list(conteo_lugares.keys())
                valores_pie_chart = list(conteo_lugares.values())


                # preparasr los datos para el grafico de barra
                empresas = [empresa['empresa_vendedora'] for empresa in empresas_valores]
                valores = [empresa['valor_unitario_min'] for empresa in empresas_valores]
                valores_float = [float(valor) for valor in valores] 



                context = {
                    'empresas': json.dumps(empresas),
                    'valores': json.dumps([float(valor) for valor in valores_float]),
                    'fechas_rental_veas': json.dumps([articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_rental_veas]),
                    'valores_unitarios_rental_veas': json.dumps([float(articulo.valor_unitario) for articulo in articulos_rental_veas]),
                    'fechas_otros': json.dumps([articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_otros]),
                    'valores_unitarios_otros': json.dumps([float(articulo.valor_unitario) for articulo in articulos_otros]),
                    'valores_pie_chart': json.dumps(valores_float), 
                    'etiquetas_pie': json.dumps(etiquetas_pie),
                    'valor_ventas_por_empresa': valor_ventas_por_empresa,
                    'volumen_ventas_por_empresa': volumen_ventas_por_empresa,
                }



                return render(request, "resultados_busqueda.html", {
                "articulos": articulos, 
                "query": producto, 
                "metricas1": metricas1,
                "metricas2": metricas2,
                "metricas3": metricas3,
                "metricas4": metricas4,
                "empresas": json.dumps(empresas),
                "valores": json.dumps(valores_float),
                "fechas_rental_veas": json.dumps(fechas_rental_veas),
                "valores_unitarios_rental_veas": json.dumps(valores_unitarios_rental_veas),
                "fechas_otros": json.dumps(fechas_otros),
                "valores_unitarios_otros": json.dumps(valores_unitarios_otros),
                "valores_pie_chart": json.dumps(valores_pie_chart),
                "etiquetas_pie": json.dumps(etiquetas_pie),
                "stock_teorico": stock_teorico,
                "resultados": resultados

                })
            else:
                return HttpResponse("No se encontraron artículos")
    else:
        return HttpResponse("No has introducido nada")




@login_required
def home_view(request):
    return render(request, 'home.html')



@login_required
def cotizacion_view(request):
    ArticuloFormSet = formset_factory(ArticuloCotizacionForm, extra=1)
    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST, prefix='cotizacion')
        articulo_formset = ArticuloFormSet(request.POST, prefix='articulo')

        if cotizacion_form.is_valid() and articulo_formset.is_valid():
            datos_cotizacion = cotizacion_form.cleaned_data

            for articulo_form in articulo_formset:
                if articulo_form.cleaned_data:  # Verifica si el formulario de artículo tiene datos
                    nuevo_articulo = articulo_form.save(commit=False)

                    # Asignar los datos de cotización a cada nuevo artículo
                    nuevo_articulo.fecha = datos_cotizacion.get('fecha')
                    nuevo_articulo.lugar = datos_cotizacion.get('lugar')
                    nuevo_articulo.vendedor = datos_cotizacion.get('vendedor')
                    nuevo_articulo.comprador = datos_cotizacion.get('comprador')
                    nuevo_articulo.empresa_compradora = datos_cotizacion.get('empresa_compradora')
                    nuevo_articulo.empresa_vendedora = datos_cotizacion.get('empresa_vendedora')
                    nuevo_articulo.forma_pago = datos_cotizacion.get('forma_pago')
                    nuevo_articulo.entrega = datos_cotizacion.get('entrega')
                    nuevo_articulo.correo_vendedor = datos_cotizacion.get('correo_vendedor')
                    nuevo_articulo.seccion = datos_cotizacion.get('seccion')

                    # Asignar los nuevos campos
                    nuevo_articulo.comentarios = datos_cotizacion.get('comentarios')
                    nuevo_articulo.aprobado = datos_cotizacion.get('aprobado')

                    # Obtener el tipo de documento para cada artículo
                    tipo_documento = datos_cotizacion.get('tipo_documento')

                    # Asignar el número de documento según el tipo seleccionado
                    if tipo_documento == 'cotizacion':
                        nuevo_articulo.numero_cotizacion = datos_cotizacion.get('numero_documento')
                    elif tipo_documento == 'boleta':
                        nuevo_articulo.numero_boleta = datos_cotizacion.get('numero_documento')
                    elif tipo_documento == 'factura':
                        nuevo_articulo.numero_factura = datos_cotizacion.get('numero_documento')

                    nuevo_articulo.save()

            return redirect('productos_agregados_correctamente')
    else:
        cotizacion_form = CotizacionForm(prefix='cotizacion')
        articulo_formset = ArticuloFormSet(prefix='articulo')

    return render(request, 'agregar_cotizacion.html', {
        'cotizacion_form': cotizacion_form,
        'articulo_formset': articulo_formset
    })

def productos_agregados_correctamente(request):
    return render(request, 'productos_agregados_correctamente.html')




@login_required
def generar_informe(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        informes_compras = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            empresa_compradora__icontains='veas',
            numero_cotizacion__isnull=True,
        ).exclude(numero_cotizacion__isnull=False)


        informes_ventas = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            empresa_vendedora='rental veas',
            numero_cotizacion__isnull=True,
        ).exclude(numero_cotizacion__isnull=False)

                
        # Calcular total de compras para cada artículo
        valores_totales_compras = []
        for articulo in informes_compras:
            total_compra = articulo.cantidad * articulo.valor_unitario
            valores_totales_compras.append((total_compra))

        # Calcular total de ventas para cada artículo
        valores_totales_ventas = []
        for articulo in informes_ventas:
            total_venta = articulo.cantidad * articulo.valor_unitario
            valores_totales_ventas.append((total_venta))

        suma_valores_totales_compras = 0
        suma_valores_totales_ventas = 0

        # Calcular total de compras
        for total_compra in valores_totales_compras:
            suma_valores_totales_compras += total_compra

        # Calcular total de ventas
        for total_venta in valores_totales_ventas:
            suma_valores_totales_ventas += total_venta

        # Calcular el balance
        balance = suma_valores_totales_ventas - suma_valores_totales_compras




        # Calcular el número de cotizaciones emitidas por la empresa vendedora que contiene "veas"
        num_cotizaciones_emitidas = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            numero_cotizacion__isnull=False,
            numero_boleta__isnull=True,
            numero_factura__isnull=True, 
            aprobado__isnull=False,           
            empresa_vendedora__icontains='veas'
        ).values('numero_cotizacion').distinct().count()

        # Calcular el número de cotizaciones aceptadas por la empresa vendedora que contiene "veas"
        num_cotizaciones_aceptadas = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            numero_cotizacion__isnull=False,
            numero_boleta__isnull=True,
            numero_factura__isnull=True,
            aprobado__isnull=False,
            empresa_vendedora__icontains='veas',
            aprobado='aprobado'
        ).values('numero_cotizacion').distinct().count()

        # Calcular el número de cotizaciones rechazadas por la empresa vendedora que contiene "veas"
        num_cotizaciones_rechazadas = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            numero_cotizacion__isnull=False,
            numero_boleta__isnull=True,
            numero_factura__isnull=True,
            aprobado__isnull=False,
            empresa_vendedora__icontains='veas',
            aprobado='rechazado'
        ).values('numero_cotizacion').distinct().count()

        # Obtener las cotizaciones rechazadas con comentarios emitidas por la empresa vendedora que contiene "veas"
        cotizaciones_rechazadas = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            numero_cotizacion__isnull=False,
            numero_boleta__isnull=True,
            numero_factura__isnull=True,
            empresa_vendedora__icontains='veas',
            aprobado__isnull=False,
            aprobado='rechazado',
            comentarios__isnull=False
        ).values_list('numero_cotizacion', 'comentarios').distinct()


        cotizaciones_rechazadas = cotizaciones_rechazadas.values_list('numero_cotizacion', 'comentarios')

        return render(request, 'informe.html', {
            'informes_compras': informes_compras,
            'informes_ventas': informes_ventas,
            'valores_totales_ventas': valores_totales_ventas,
            'valores_totales_compras': valores_totales_compras,
            'suma_valores_totales_ventas': suma_valores_totales_ventas,
            'suma_valores_totales_compras': suma_valores_totales_compras,
            'balance': balance,
            'num_cotizaciones_emitidas': num_cotizaciones_emitidas,
            'num_cotizaciones_aceptadas': num_cotizaciones_aceptadas,
            'num_cotizaciones_rechazadas': num_cotizaciones_rechazadas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'cotizaciones_rechazadas': cotizaciones_rechazadas,
        })
    
    
    return render(request, 'generar_informe.html')








