from rest_framework import serializers
from .models import ActivoUbicacion, Activo, Medicamento
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class ActivoUbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivoUbicacion
        fields = ('nombre',)

class ActivoSerializer(serializers.ModelSerializer):
    ubicacion = serializers.ReadOnlyField(source='ubicacion.nombre')
    class Meta:
        model = Activo
        fields = '__all__'


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
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


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(source='first_name', required=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'name')
        
    def validate(self, attrs):
        # Check if email already exists
        User = get_user_model()
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})
            
        return attrs
        
    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user