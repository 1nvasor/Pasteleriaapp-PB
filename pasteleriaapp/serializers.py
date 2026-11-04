from rest_framework import serializers
from .models import Producto


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
