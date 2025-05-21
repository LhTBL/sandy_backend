from rest_framework import serializers
from .models import ActivoUbicacion, Activo

class ActivoUbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivoUbicacion
        fields = ('nombre',)

class ActivoSerializer(serializers.ModelSerializer):
    ubicacion = serializers.ReadOnlyField(source='ubicacion.nombre')
    class Meta:
        model = Activo
        fields = '__all__'
