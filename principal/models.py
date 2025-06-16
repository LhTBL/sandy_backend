from django.db import models

class ActivoUbicacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

class Activo(models.Model):
    ACTIVO_ESTADO_CHOICES = (
        ('Operativo', 'Operativo'),
        ('Mantenimiento', 'Mantenimiento'),
        ('No Operativo', 'No Operativo'),
        ('Otro', 'Otro'),
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=100)
    estado = models.CharField(max_length=100, choices=ACTIVO_ESTADO_CHOICES)
    comentarios = models.TextField(max_length=100)
    responsable = models.CharField(max_length=100)
    ubicacion = models.ForeignKey(ActivoUbicacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=100)
    fecha_vencimiento = models.DateField()
    cantidad = models.PositiveIntegerField()
    imagen_url = models.URLField()

    def __str__(self):
        return self.nombre