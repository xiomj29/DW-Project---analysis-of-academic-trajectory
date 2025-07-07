# warehouse/models.py
from django.db import models

class DimEstudiante(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    carrera = models.CharField(max_length=100, null=True, blank=True)
    semestre = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dim_estudiante'
        managed = False

class DimMateria(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre_materia = models.CharField(max_length=100, null=True, blank=True)
    codigo_materia = models.CharField(max_length=20, null=True, blank=True)
    creditos = models.IntegerField(null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'dim_materia'
        managed = False

class DimProfesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre_profesor = models.CharField(max_length=100, null=True, blank=True)
    apellido_profesor = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'dim_profesor'
        managed = False

class DimTiempo(models.Model):
    id_tiempo = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True, blank=True)
    mes = models.CharField(max_length=20, null=True, blank=True)
    semestre = models.CharField(max_length=20, null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    periodo_academico = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'dim_tiempo'
        managed = False

class DimEscuela(models.Model):
    id_escuela = models.AutoField(primary_key=True)
    nombre_escuela = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'dim_escuela'
        managed = False

class HechosCalificaciones(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(DimEstudiante, db_column='id_estudiante', on_delete=models.DO_NOTHING)
    id_materia = models.ForeignKey(DimMateria, db_column='id_materia', on_delete=models.DO_NOTHING)
    id_profesor = models.ForeignKey(DimProfesor, db_column='id_profesor', on_delete=models.DO_NOTHING)
    id_tiempo = models.ForeignKey(DimTiempo, db_column='id_tiempo', on_delete=models.DO_NOTHING)
    id_escuela = models.ForeignKey(DimEscuela, db_column='id_escuela', on_delete=models.DO_NOTHING)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    puntos_obtenidos = models.IntegerField(null=True, blank=True)
    puntos_totales = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'hechos_calificaciones'
        managed = False