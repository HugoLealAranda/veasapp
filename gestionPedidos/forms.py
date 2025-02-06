from django import forms
from django.core.exceptions import ValidationError
from gestionPedidos.models import Articulos, Tarea

# 1) FORMULARIO DE ARTÍCULO
class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields = [
            'nombre', 'cantidad', 'unidad', 'valor_unitario',
            'fecha', 'lugar', 'vendedor', 'comprador',
            'empresa_compradora', 'empresa_vendedora', 'forma_pago',
            'entrega', 'correo_vendedor', 'seccion', 'numero_boleta'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del artículo'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad (ej. caja, kilo, etc.)'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar de la compra/venta'}),
            'vendedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendedor'}),
            'comprador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comprador'}),
            'empresa_compradora': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa compradora'}),
            'empresa_vendedora': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa vendedora'}),
            'forma_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Forma de pago'}),
            'entrega': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo o lugar de entrega'}),
            'correo_vendedor': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'seccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sección'}),
            'numero_boleta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de boleta/factura'}),
        }

# 2) FORMULARIO DE COTIZACIÓN
class CotizacionForm(forms.Form):
    TIPO_DOCUMENTO_CHOICES = [
        ('cotizacion', 'Cotización'),
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    ]

    tipo_documento = forms.ChoiceField(
        label="Tipo de documento", 
        choices=TIPO_DOCUMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    numero_documento = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° de documento'})
    )
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'})
    )
    lugar = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar'})
    )
    vendedor = forms.CharField(
        label="Nombre de vendedor",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    comprador = forms.CharField(
        label="Nombre de comprador",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    empresa_compradora = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    empresa_vendedora = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    forma_pago = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    entrega = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    seccion = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    comentarios = forms.CharField(
        label="Comentarios",
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 25,
            'class': 'form-control',
            'placeholder': 'Comentarios adicionales'
        })
    )
    aprobado = forms.ChoiceField(
        label="Aprobado/Rechazado",
        choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    correo_vendedor = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )

# 3) FORMULARIO DE TAREA
class TareaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].validators.append(self.validate_descripcion_length)
        # Opcional: asignar clase form-control desde el __init__:
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_vencimiento'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['completada'].widget.attrs.update({'class': 'form-check-input'})  # Para checkbox

    def validate_descripcion_length(self, value):
        if len(value) > 50:
            raise ValidationError('La descripción no puede tener más de 50 caracteres.')

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento', 'completada']

# 4) FORMULARIO DE ARTÍCULO PARA COTIZACIÓN
class ArticuloCotizacionForm(forms.ModelForm):
    UNIDAD_CHOICES = [
        ('unidad', 'Unidad'),
        ('bolsa', 'Bolsa'),
        ('caja', 'Caja'),
        ('galon', 'Galón'),
        ('kilo', 'Kilo'),
        ('litro', 'Litro'),
        ('metro', 'Metro'),
        ('rollo', 'Rollo'),
        ('tira', 'Tira'),
    ]

    unidad = forms.ChoiceField(
        label="Unidad",
        choices=UNIDAD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Articulos
        fields = ['nombre', 'cantidad', 'valor_unitario', 'unidad']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
             }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'valor_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }

