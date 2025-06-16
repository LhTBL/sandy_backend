from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivoUbicacionViewSet, ActivoViewSet, MedicamentoViewSet, generar_reporte, preview_reporte

router = DefaultRouter()
router.register(r'ubicaciones', ActivoUbicacionViewSet)
router.register(r'activos', ActivoViewSet)
router.register(r'medicamentos', MedicamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reportes/generar', generar_reporte, name='generar_reporte'),
    path('reportes/preview', preview_reporte, name='preview_reporte'),
]
