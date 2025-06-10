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


class DateRangeSerializer(serializers.Serializer):
    startDate = serializers.DateField(required=False, allow_null=True)
    endDate = serializers.DateField(required=False, allow_null=True)


class ReportRequestSerializer(serializers.Serializer):
    REPORT_TYPES = (
        ('activos', 'Activos'),
        ('mantenimiento', 'Mantenimiento'),
        ('bajas', 'Bajas'),
        ('responsables', 'Responsables'),
    )

    FILTER_TYPES = (
        ('all', 'Todos'),
        ('operativo', 'Operativo'),
        ('mantenimiento', 'Mantenimiento'),
        ('fuera', 'Fuera de servicio'),
    )

    reportType = serializers.ChoiceField(choices=REPORT_TYPES)
    dateRange = DateRangeSerializer()
    filter = serializers.ChoiceField(choices=FILTER_TYPES)

    def validate_dateRange(self, value):
        start_date = value.get('startDate')
        end_date = value.get('endDate')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha final")
        return value