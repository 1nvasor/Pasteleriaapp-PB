from django import forms
from .models import Producto

# Formulario para CREAR
class ProductoCrearForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'descripcion', 'precio', 'stock', 'correo_proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. Torta Amor',
                'maxlength': '50'  # <-- Bloquea el texto a 50 caracteres máximo
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': '200'}),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. 18000',
                'max': '999999',         # <-- Valor número máximo aceptado por el navegador
                'oninput': 'if(this.value.length > 6) this.value = this.value.slice(0, 6);' # <-- Trunca si escribe más de 6 dígitos
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. 10',
                'max': '9999',           # <-- Máximo 4 dígitos
                'oninput': 'if(this.value.length > 4) this.value = this.value.slice(0, 4);'
            }),
            'correo_proveedor': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'proveedor@gmail.com',
                'maxlength': '80'
            }),
        }

def clean_correo_proveedor(self):
    email = self.cleaned_data.get('correo_proveedor')
    if email and not email.endswith('@gmail.com'):
        raise forms.ValidationError("El correo del proveedor debe ser obligatoriamente una cuenta de @gmail.com.")
    return email

def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio <= 0:
                raise forms.ValidationError("El precio debe ser mayor a $0.")
            
            # Limite de longitud (ejemplo: máximo 6 dígitos)
            if len(str(precio)) > 6:
                raise forms.ValidationError("El precio no puede tener más de 6 dígitos.")
                
        return precio

def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None:
            if stock < 0:
                raise forms.ValidationError("El stock no puede ser un número negativo.")
                
            # Limite de longitud (ejemplo: máximo 4 dígitos)
            if len(str(stock)) > 4:
                raise forms.ValidationError("El stock no puede tener más de 4 dígitos.")
                
        return stock


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

