from django import forms
from gestionPedidos.models import Articulos


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields = ['nombre', 'cantidad', 'unidad', 'valor_unitario', 'fecha', 'lugar', 'vendedor', 'comprador', 'empresa_compradora', 'empresa_vendedora', 'forma_pago', 'entrega', 'correo_vendedor', 'seccion', 'numero_boleta']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class CotizacionForm(forms.Form):
    TIPO_DOCUMENTO_CHOICES = [
        ('cotizacion', 'Cotización'),
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    ]
    tipo_documento = forms.ChoiceField(label="Tipo de documento", choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = forms.CharField(max_length=100, required=False)
    fecha = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), required=False)
    lugar = forms.CharField(max_length=100, required=False)
    vendedor = forms.CharField(label="Nombre de vendedor", max_length=100, required=False)
    comprador = forms.CharField(label="Nombre de comprador", max_length=100, required=False)
    empresa_compradora = forms.CharField(max_length=100, required=False)
    empresa_vendedora = forms.CharField(max_length=100, required=False)
    forma_pago = forms.CharField(max_length=100, required=False)
    entrega = forms.CharField(max_length=100, required=False)
    correo_vendedor = forms.EmailField(required=False)

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

    unidad = forms.ChoiceField(label="Unidad", choices=UNIDAD_CHOICES)

    class Meta:
        model = Articulos
        fields = ['nombre', 'cantidad',  'valor_unitario','unidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'field-xlarge'}),  
            'cantidad': forms.NumberInput(attrs={'class': 'field-small'}),  
            'valor_unitario': forms.NumberInput(attrs={'class': 'field-small'}),  
        }



