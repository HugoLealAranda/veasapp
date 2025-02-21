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



import html
from django.http import HttpResponse
from django.shortcuts import render, redirect
from collections import Counter
from .models import Articulos
from django.forms import formset_factory
from django.db.models import Avg, Min, Max, Count, Sum, F, FloatField
from django.db.models.functions import Round
import matplotlib
matplotlib.use('Agg')
import json
from .forms import CotizacionForm, ArticuloCotizacionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from gestionPedidos.models import Message
from .models import Tarea

# ... Otras views ...

@login_required
def buscar(request):
    if 'prd' in request.GET and request.GET['prd']:
        # Obtener el parámetro de búsqueda
        producto = request.GET['prd']
        # Decodificar entidades HTML para que "1&quot;o" se convierta en '1"o'
        producto = html.unescape(producto)
        
        if len(producto) > 100:
            return HttpResponse("Texto de búsqueda demasiado largo")
        else:
            # Realiza la búsqueda usando el valor decodificado
            articulos = Articulos.objects.filter(nombre__icontains=producto).order_by('fecha')
            if articulos.exists():
                empresas_valores = articulos.exclude(empresa_vendedora__iexact='rental veas') \
                                            .values('empresa_vendedora') \
                                            .annotate(valor_unitario_min=Min('valor_unitario'))

                ultimo_articulo_otros = articulos.exclude(empresa_vendedora__iexact='rental veas').order_by('-fecha').first()
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

                resultados = []
                for transaccion in transacciones_recientes:
                    empresa = transaccion['empresa_vendedora']
                    transaccion_mas_reciente = Articulos.objects.filter(
                        empresa_vendedora=empresa,
                        fecha=transaccion['ultima_transaccion'],
                        entrega__isnull=False,
                        nombre__icontains=producto
                    ).first()
                    if transaccion_mas_reciente:
                        resultados.append({
                            'empresa_vendedora': empresa,
                            'entrega': transaccion_mas_reciente.entrega
                        })

                volumen_ventas_por_empresa = Articulos.objects.exclude(empresa_vendedora__iexact='rental veas') \
                                            .filter(numero_cotizacion__isnull=True) \
                                            .filter(nombre__icontains=producto) \
                                            .values('empresa_vendedora') \
                                            .annotate(volumen_total=Sum('cantidad')) \
                                            .order_by('-volumen_total')

                valor_ventas_por_empresa = articulos.exclude(empresa_vendedora__iexact='rental veas') \
                                                    .filter(numero_cotizacion__isnull=True) \
                                                    .annotate(valor_total=F('cantidad') * F('valor_unitario')) \
                                                    .values('empresa_vendedora') \
                                                    .annotate(valor_total_sum=Sum('valor_total', output_field=FloatField())) \
                                                    .order_by('-valor_total_sum')

                rendimiento_compradores = articulos.filter(numero_cotizacion__isnull=True) \
                                                    .filter(nombre__icontains=producto) \
                                                    .values('comprador') \
                                                    .annotate(total_comprado=Sum('cantidad'), 
                                                              valor_total_comprado=Sum(F('cantidad') * F('valor_unitario'))) \
                                                    .order_by('-total_comprado')
                
                compras_totales_veas = Articulos.objects.exclude(empresa_vendedora__iexact='Rental Veas') \
                                                        .filter(numero_cotizacion__isnull=True) \
                                                        .filter(nombre__icontains=producto) \
                                                        .values('empresa_vendedora') \
                                                        .annotate(volumen_total=Sum('cantidad')) \
                                                        .order_by('-volumen_total')
                
                ventas_totales_veas = Articulos.objects.filter(empresa_vendedora__iexact='Rental Veas') \
                                                        .filter(numero_cotizacion__isnull=True) \
                                                        .filter(nombre__icontains=producto) \
                                                        .values('empresa_vendedora') \
                                                        .annotate(volumen_total=Sum('cantidad')) \
                                                        .order_by('-volumen_total')

                total_compras_veas = sum(item['volumen_total'] for item in compras_totales_veas)
                total_ventas_veas = sum(item['volumen_total'] for item in ventas_totales_veas)
                stock_teorico = total_compras_veas - total_ventas_veas

                ultimo_valor_venta_rental_veas = articulos.filter(numero_cotizacion__isnull=True).filter(empresa_vendedora='rental veas').order_by('-fecha').first()
                valor_unitario_venta_rental_veas = ultimo_valor_venta_rental_veas.valor_unitario if ultimo_valor_venta_rental_veas else 0

                ultimo_valor_compra_rental_veas = articulos.filter(numero_cotizacion__isnull=True).filter(empresa_compradora='rental veas').order_by('-fecha').first()
                valor_unitario_compra_rental_veas = ultimo_valor_compra_rental_veas.valor_unitario if ultimo_valor_compra_rental_veas else 0

                ultimo_valor_cotizado_rental_veas = articulos.exclude(numero_cotizacion__isnull=True).filter(empresa_compradora='rental veas').order_by('-fecha').first()
                valor_unitario_cotizado_rental_veas = ultimo_valor_cotizado_rental_veas.valor_unitario if ultimo_valor_cotizado_rental_veas else 0

                ultimo_valor_cotizado_proveedores = articulos.exclude(numero_cotizacion__isnull=True).filter(empresa_vendedora='rental veas').order_by('-fecha').first()
                valor_unitario_cotizado_proveedores = ultimo_valor_cotizado_proveedores.valor_unitario if ultimo_valor_cotizado_proveedores else 0

                articulos_venta_rental_veas = articulos.filter(numero_cotizacion__isnull=True, empresa_vendedora__iexact='rental veas')
                promedio_venta_valor_unitario = articulos_venta_rental_veas.aggregate(promedio=Avg('valor_unitario'))['promedio']
                promedio_venta_valor_unitario = round(promedio_venta_valor_unitario, 2) if promedio_venta_valor_unitario is not None else 0

                articulos_compra_rental_veas = articulos.filter(numero_cotizacion__isnull=True, empresa_compradora__iexact='rental veas')
                promedio_compra_valor_unitario = articulos_compra_rental_veas.aggregate(promedio=Avg('valor_unitario'))['promedio']
                promedio_compra_valor_unitario = round(promedio_compra_valor_unitario, 2) if promedio_compra_valor_unitario is not None else 0

                utilidad_ultima_compraventa = valor_unitario_venta_rental_veas - valor_unitario_compra_rental_veas
                utilidad_promedio_historica = promedio_venta_valor_unitario - promedio_compra_valor_unitario

                metricas1 = {
                    'valor_unitario_venta_rental_veas': valor_unitario_venta_rental_veas,
                    'valor_unitario_compra_rental_veas': valor_unitario_compra_rental_veas,
                    'valor_unitario_cotizado_rental_veas': valor_unitario_cotizado_rental_veas,
                    'valor_unitario_cotizado_proveedores': valor_unitario_cotizado_proveedores,
                    'ultimo_valor_otros': ultimo_valor_otros,
                    'promedio_compra_valor_unitario': promedio_compra_valor_unitario,
                    'promedio_venta_valor_unitario': promedio_venta_valor_unitario,
                    'rendimiento_compradores': rendimiento_compradores,
                    'utilidad_ultima_compraventa': utilidad_ultima_compraventa,
                    'utilidad_promedio_historica': utilidad_promedio_historica,
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
                
                articulos_compra_rental_veas = articulos.filter(empresa_compradora='rental veas').exclude(numero_cotizacion__isnull=True).exclude(fecha__isnull=True)
                fechas_compra_rental_veas = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_compra_rental_veas]
                valores_unitarios_compra_rental_veas = [float(articulo.valor_unitario) for articulo in articulos_compra_rental_veas]
                numeros_documentos_compra_rental_veas = [articulo.numero_cotizacion or articulo.numero_factura or articulo.numero_boleta for articulo in articulos_compra_rental_veas]

                articulos_venta_rental_veas = articulos.filter(empresa_vendedora='rental veas').exclude(numero_cotizacion__isnull=True).exclude(fecha__isnull=True)
                fechas_venta_rental_veas = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_venta_rental_veas]
                valores_unitarios_venta_rental_veas = [float(articulo.valor_unitario) for articulo in articulos_venta_rental_veas]
                numeros_documentos_venta_rental_veas = [articulo.numero_cotizacion or articulo.numero_factura or articulo.numero_boleta for articulo in articulos_venta_rental_veas]

                articulos_cotizacion_rental_veas = articulos.exclude(numero_cotizacion__isnull=True).filter(empresa_vendedora='rental veas').exclude(fecha__isnull=True)
                fechas_cotizacion_rental_veas = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_cotizacion_rental_veas]
                valores_unitarios_cotizacion_rental_veas = [float(articulo.valor_unitario) for articulo in articulos_cotizacion_rental_veas]
                numeros_documentos_cotizacion_rental_veas = [articulo.numero_cotizacion or articulo.numero_factura or articulo.numero_boleta for articulo in articulos_cotizacion_rental_veas]

                articulos_cotizacion_proveedores = articulos.exclude(numero_cotizacion__isnull=True).filter(empresa_compradora='rental veas').exclude(fecha__isnull=True)
                fechas_cotizacion_proveedores = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_cotizacion_proveedores]
                valores_unitarios_cotizacion_proveedores = [float(articulo.valor_unitario) for articulo in articulos_cotizacion_proveedores]
                numeros_documentos_cotizacion_proveedores = [articulo.numero_cotizacion or articulo.numero_factura or articulo.numero_boleta for articulo in articulos_cotizacion_proveedores]

                fechas_rental_veas = []
                valores_unitarios_rental_veas = []
                articulos_rental_veas = articulos.filter(empresa_vendedora='rental veas').exclude(fecha__isnull=True)

                if articulos_rental_veas:
                    fechas_rental_veas = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_rental_veas]
                    valores_unitarios_rental_veas = [float(articulo.valor_unitario) for articulo in articulos_rental_veas] 
                fechas_otros = []
                valores_unitarios_otros = []
                articulos_otros = articulos.exclude(empresa_vendedora='rental veas').exclude(fecha__isnull=True)

                if articulos_otros:
                    fechas_otros = [articulo.fecha.strftime('%Y-%m-%d') for articulo in articulos_otros]
                    valores_unitarios_otros = [float(articulo.valor_unitario) for articulo in articulos_otros]

                lugares = [articulo.lugar for articulo in articulos if articulo.lugar]
                conteo_lugares = Counter(lugares)
                etiquetas_pie = list(conteo_lugares.keys())
                valores_pie_chart = list(conteo_lugares.values())

                empresas = [empresa['empresa_vendedora'] for empresa in empresas_valores]
                valores = [empresa['valor_unitario_min'] for empresa in empresas_valores]
                valores_float = [float(valor) for valor in valores]

                return render(request, "resultados_busqueda.html", {
                    "articulos": articulos, 
                    "query": producto, 
                    "metricas1": metricas1,
                    "metricas2": metricas2,
                    "metricas3": metricas3,
                    "metricas4": metricas4,
                    "empresas": json.dumps(empresas),
                    "valores": json.dumps(valores_float),
                    "fechas_compra_rental_veas": json.dumps(fechas_compra_rental_veas),
                    "valores_unitarios_compra_rental_veas": json.dumps(valores_unitarios_compra_rental_veas),
                    "fechas_venta_rental_veas": json.dumps(fechas_venta_rental_veas),
                    "valores_unitarios_venta_rental_veas": json.dumps(valores_unitarios_venta_rental_veas),
                    "fechas_cotizacion_rental_veas": json.dumps(fechas_cotizacion_rental_veas),
                    "valores_unitarios_cotizacion_rental_veas": json.dumps(valores_unitarios_cotizacion_rental_veas),
                    "numeros_documentos_compra_rental_veas": json.dumps(numeros_documentos_compra_rental_veas),
                    "numeros_documentos_venta_rental_veas": json.dumps(numeros_documentos_venta_rental_veas),
                    "numeros_documentos_cotizacion_rental_veas": json.dumps(numeros_documentos_cotizacion_rental_veas),
                    "fechas_cotizacion_proveedores": json.dumps(fechas_cotizacion_proveedores),
                    "valores_unitarios_cotizacion_proveedores": json.dumps(valores_unitarios_cotizacion_proveedores),
                    "numeros_documentos_cotizacion_proveedores": json.dumps(numeros_documentos_cotizacion_proveedores),
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

        # Obtener informes de ventas
        informes_ventas = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            cantidad__isnull=False,
            valor_unitario__isnull=False,
            empresa_vendedora__icontains='veas',
            numero_factura__isnull=False,
        )

        # Obtener informes de compras
        informes_compras = Articulos.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin],
            cantidad__isnull=False,
            valor_unitario__isnull=False,
            empresa_compradora__icontains='veas',
            numero_factura__isnull=False,
        )

        # Lista de informes de ventas con sus propiedades
        lista_informes_ventas = [[informe.nombre, informe.cantidad, informe.valor_unitario, informe.cantidad * informe.valor_unitario] for informe in informes_ventas]

        # Lista de informes de compras con sus propiedades
        lista_informes_compras = [[informe.nombre, informe.cantidad, informe.valor_unitario, informe.cantidad * informe.valor_unitario] for informe in informes_compras]


        # Calcular total de compras
        suma_valores_totales_compras = sum(informe[3] for informe in lista_informes_compras)

        # Calcular total de ventas
        suma_valores_totales_ventas = sum(informe[3] for informe in lista_informes_ventas)


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
            'lista_informes_compras': lista_informes_compras,
            'lista_informes_ventas': lista_informes_ventas,
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



from django.http import JsonResponse
from django.db.models import Q
from .models import Articulos  # Asegúrate de importar tu modelo

def buscar_articulos_nombres(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(nombre__icontains=term)\
                                  .values_list('nombre', flat=True)\
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)


# views.py

from django.http import JsonResponse
from django.db.models import Q
from .models import Articulos

def buscar_lugares(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(lugar__icontains=term) \
                                  .values_list('lugar', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_vendedores(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(vendedor__icontains=term) \
                                  .values_list('vendedor', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_compradores(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(comprador__icontains=term) \
                                  .values_list('comprador', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_empresas_compradoras(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(empresa_compradora__icontains=term) \
                                  .values_list('empresa_compradora', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_empresas_vendedoras(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(empresa_vendedora__icontains=term) \
                                  .values_list('empresa_vendedora', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_formas_pago(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(forma_pago__icontains=term) \
                                  .values_list('forma_pago', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_entregas(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(entrega__icontains=term) \
                                  .values_list('entrega', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_secciones(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(seccion__icontains=term) \
                                  .values_list('seccion', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)

def buscar_correos_vendedor(request):
    term = request.GET.get('term', '')
    resultados = Articulos.objects.filter(correo_vendedor__icontains=term) \
                                  .values_list('correo_vendedor', flat=True) \
                                  .distinct()[:20]
    return JsonResponse(list(resultados), safe=False)






#creado por hugo francisco leal aranda