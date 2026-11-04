from rest_framework import serializers
from .models import Producto

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