from django.db import models
from django.core.validators import MinValueValidator, EmailValidator

class Producto(models.Model):
    CATEGORIAS = [
        ('Tortas', 'Tortas y Pasteles'),
        ('Pie', 'Pies y Tartas'),
        ('Postres', 'Postres Individuales'),
        ('Galletas', 'Galletas y Pastelería Fina'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del Pastel/Producto")
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='Tortas', verbose_name="Categoría")
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    
    # Validación
    precio = models.IntegerField(
        validators=[MinValueValidator(1, message="El precio debe ser mayor a $0.")],
        verbose_name="Precio ($)"
    )
    
    # Validación: Stock 
    stock = models.IntegerField(
        validators=[MinValueValidator(0, message="El stock no puede ser negativo.")],
        verbose_name="Stock disponible"
    )
    
    # Validación de Correo 
    correo_proveedor = models.EmailField(
        validators=[EmailValidator(message="Ingrese un correo electrónico válido.")],
        verbose_name="Correo del Proveedor/Repostero"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
