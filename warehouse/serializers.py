# warehouse/serializers.py
from rest_framework import serializers
from .models import HechosCalificaciones, DimEstudiante, DimMateria, DimProfesor, DimTiempo, DimEscuela

class DimEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimEstudiante
        fields = ['id_estudiante', 'nombre', 'apellido', 'carrera', 'semestre']

class DimMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimMateria
        fields = ['id_materia', 'nombre_materia', 'codigo_materia', 'creditos', 'departamento']

class DimProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimProfesor
        fields = ['id_profesor', 'nombre_profesor', 'apellido_profesor', 'departamento']

class DimTiempoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimTiempo
        fields = ['id_tiempo', 'fecha', 'mes', 'semestre', 'anio', 'periodo_academico']

class DimEscuelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimEscuela
        fields = ['id_escuela', 'nombre_escuela']

class HechosCalificacionesSerializer(serializers.ModelSerializer):
    id_estudiante = DimEstudianteSerializer(read_only=True)
    id_materia = DimMateriaSerializer(read_only=True)
    id_profesor = DimProfesorSerializer(read_only=True)
    id_tiempo = DimTiempoSerializer(read_only=True)
    id_escuela = DimEscuelaSerializer(read_only=True)

    class Meta:
        model = HechosCalificaciones
        fields = [
            'id_calificacion',
            'id_estudiante',
            'id_materia',
            'id_profesor',
            'id_tiempo',
            'id_escuela',
            'calificacion',
            'puntos_obtenidos',
            'puntos_totales',
        ]