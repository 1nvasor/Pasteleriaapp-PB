from rest_framework import serializers
from .models import Producto

<<<<<<< HEAD

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'descripcion', 'precio', 'stock', 'correo_proveedor', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        if len(str(value)) > 6:
            raise serializers.ValidationError("El precio no puede superar los 6 dígitos.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        if len(str(value)) > 4:
            raise serializers.ValidationError("El stock no puede superar los 4 dígitos.")
        return value

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'categoria',
            'descripcion',
            'precio',
            'stock',
            'correo_proveedor',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'fecha_creacion']
=======
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    # Validación personalizada de nombre (entre 3 y 30 caracteres)
    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if len(value) > 30:
            raise serializers.ValidationError("El nombre no puede superar los 30 caracteres.")
        return value
>>>>>>> 6d1dce2a47393e8f2bca6929c82b880fffecae1c
