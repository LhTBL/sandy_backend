from django.contrib import admin

from principal.models import Activo, ActivoUbicacion


@admin.register(ActivoUbicacion)
class ActivoUbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', )

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'comentarios', 'responsable')
    search_fields = ('nombre', 'estado', 'comentarios', 'responsable')
    list_filter = ('estado', 'responsable')

