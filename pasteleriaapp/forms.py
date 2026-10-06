from django import forms
from .models import Producto

# Formulario para CREAR
class ProductoCrearForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'descripcion', 'precio', 'stock', 'correo_proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Torta Amor'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción breve del producto...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 18000'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 10'}),
            'correo_proveedor': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'proveedor@pasteleria.cl'}),
        }

# Formulario para EDITAR 
class ProductoEditarForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'descripcion', 'precio', 'stock', 'correo_proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control bg-light', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'correo_proveedor': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'nombre': 'Modifique el nombre solo si es necesario.',
            'stock': 'Actualice la cantidad disponible en inventario.',
        }