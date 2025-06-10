from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import ActivoUbicacion, Activo
from .serializers import ActivoUbicacionSerializer, ActivoSerializer, ReportRequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import io
from django.http import FileResponse
from datetime import datetime

# Create your views here.

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        User = get_user_model()
        # Try to get full name, fallback to username
        name = getattr(user, 'get_full_name', lambda: None)() or user.username
        # Try to get role if it exists
        role = getattr(user, 'role', None)
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': name,
        }
        if role:
            data['role'] = role
        return Response(data)

# CRUD API viewsets
class ActivoUbicacionViewSet(viewsets.ModelViewSet):
    queryset = ActivoUbicacion.objects.all()
    serializer_class = ActivoUbicacionSerializer

class ActivoViewSet(viewsets.ModelViewSet):
    queryset = Activo.objects.all()
    serializer_class = ActivoSerializer


@api_view(['POST'])
def generar_reporte(request):
    """
    Genera un reporte en formato Excel basado en los parámetros proporcionados.
    """
    serializer = ReportRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    report_type = serializer.validated_data['reportType']
    date_range = serializer.validated_data['dateRange']
    filter_type = serializer.validated_data['filter']

    # Obtener datos según el tipo de reporte
    data_frame = get_report_data(report_type, date_range, filter_type)

    if data_frame is None or data_frame.empty:
        return Response({"error": "No hay datos para los criterios seleccionados"},
                        status=status.HTTP_404_NOT_FOUND)

    # Generar archivo Excel
    buffer = io.BytesIO()
    data_frame.to_excel(buffer, index=False)
    buffer.seek(0)

    # Nombre del archivo con fecha actual
    filename = f"reporte_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@api_view(['POST'])
def preview_reporte(request):
    """
    Devuelve una vista previa de los datos que se incluirán en el reporte.
    """
    serializer = ReportRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    report_type = serializer.validated_data['reportType']
    date_range = serializer.validated_data['dateRange']
    filter_type = serializer.validated_data['filter']

    # Obtener datos según el tipo de reporte
    data_frame = get_report_data(report_type, date_range, filter_type)

    if data_frame is None or data_frame.empty:
        return Response({
            "columns": [],
            "rows": []
        })

    # Convertir DataFrame a formato esperado por el frontend
    columns = data_frame.columns.tolist()
    rows = data_frame.values.tolist()

    return Response({
        "columns": columns,
        "rows": rows
    })


def get_report_data(report_type, date_range, filter_type):
    """
    Obtiene los datos para el reporte según los criterios especificados.
    Retorna un DataFrame de pandas con los datos.
    """
    # Extraer fechas del rango
    start_date = date_range.get('startDate')
    end_date = date_range.get('endDate')

    # Reporte de activos
    if report_type == 'activos':
        queryset = Activo.objects.all()

        # Aplicar filtro según el estado
        if filter_type == 'operativo':
            queryset = queryset.filter(estado='operativo')
        elif filter_type == 'mantenimiento':
            queryset = queryset.filter(estado='mantenimiento')
        elif filter_type == 'fuera':
            queryset = queryset.filter(estado='fuera_servicio')

        # Convertir queryset a DataFrame
        data = list(queryset.values(
            'codigo', 'nombre', 'descripcion', 'estado', 'fecha_adquisicion',
            'valor_adquisicion'
        ))

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        # Renombrar columnas para mejor visualización
        df = df.rename(columns={
            'codigo': 'Código',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'fecha_adquisicion': 'Fecha de Adquisición',
            'valor_adquisicion': 'Valor de Adquisición'
        })

        # Agregar información de responsable si está disponible
        try:
            df['Responsable'] = queryset.values_list('responsable__nombre', flat=True)
        except:
            pass

    # Para los reportes de mantenimiento y bajas necesitaríamos implementar
    # la lógica específica según los modelos disponibles
    elif report_type == 'mantenimiento':
        # Implementar lógica para reporte de mantenimiento
        # Como ejemplo, usamos datos dummy
        df = pd.DataFrame({
            'Activo': ['Computadora', 'Impresora'],
            'Fecha': ['2025-05-01', '2025-06-01'],
            'Tipo': ['Preventivo', 'Correctivo'],
            'Costo': [500, 1200]
        })

    elif report_type == 'bajas':
        # Implementar lógica para reporte de bajas
        # Como ejemplo, usamos datos dummy
        df = pd.DataFrame({
            'Activo': ['Monitor', 'Scanner'],
            'Fecha de Baja': ['2025-04-15', '2025-05-20'],
            'Motivo': ['Obsolescencia', 'Daño'],
            'Valor Recuperado': [0, 150]
        })

    else:
        return None

    return df