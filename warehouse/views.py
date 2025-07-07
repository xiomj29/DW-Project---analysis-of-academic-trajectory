# warehouse/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import transaction

from .models import (
    DimEstudiante, DimMateria, DimProfesor, DimTiempo, DimEscuela, HechosCalificaciones
)
from .serializers import (
    DimEstudianteSerializer, DimMateriaSerializer, DimProfesorSerializer,
    DimTiempoSerializer, DimEscuelaSerializer, HechosCalificacionesSerializer
)

# Vista para obtener calificaciones filtradas por estudiante
class CalificacionesEstudianteView(APIView):
    def get(self, request, id_estudiante):
        calificaciones = HechosCalificaciones.objects.filter(id_estudiante__id_estudiante=id_estudiante)
        
        if not calificaciones.exists():
            return Response({"error": "No se encontraron calificaciones para el estudiante."}, status=status.HTTP_404_NOT_FOUND)

        serializer = HechosCalificacionesSerializer(calificaciones, many=True)
        return Response(serializer.data)


# Vista para carga masiva de datos
class LoadDataView(APIView):
    """
    Vista para cargar datos en las tablas del Data Warehouse.
    Espera un JSON con listas de registros para cada tabla dimensional y hechos.
    """

    def post(self, request):
        data = request.data

        try:
            with transaction.atomic():
                # Cargar estudiantes
                estudiantes = data.get('estudiantes', [])
                for est in estudiantes:
                    DimEstudiante.objects.update_or_create(
                        id_estudiante=est.get('id_estudiante'),
                        defaults={
                            'nombre': est.get('nombre'),
                            'apellido': est.get('apellido'),
                            'carrera': est.get('carrera'),
                            'semestre': est.get('semestre'),
                        }
                    )

                # Cargar materias
                materias = data.get('materias', [])
                for mat in materias:
                    DimMateria.objects.update_or_create(
                        id_materia=mat.get('id_materia'),
                        defaults={
                            'nombre_materia': mat.get('nombre_materia'),
                            'codigo_materia': mat.get('codigo_materia'),
                            'creditos': mat.get('creditos'),
                            'departamento': mat.get('departamento'),
                        }
                    )

                # Cargar profesores
                profesores = data.get('profesores', [])
                for prof in profesores:
                    DimProfesor.objects.update_or_create(
                        id_profesor=prof.get('id_profesor'),
                        defaults={
                            'nombre_profesor': prof.get('nombre_profesor'),
                            'apellido_profesor': prof.get('apellido_profesor'),
                            'departamento': prof.get('departamento'),
                        }
                    )

                # Cargar tiempos
                tiempos = data.get('tiempos', [])
                for t in tiempos:
                    DimTiempo.objects.update_or_create(
                        id_tiempo=t.get('id_tiempo'),
                        defaults={
                            'fecha': t.get('fecha'),
                            'mes': t.get('mes'),
                            'semestre': t.get('semestre'),
                            'anio': t.get('anio'),
                            'periodo_academico': t.get('periodo_academico'),
                        }
                    )

                # Cargar escuelas
                escuelas = data.get('escuelas', [])
                for esc in escuelas:
                    DimEscuela.objects.update_or_create(
                        id_escuela=esc.get('id_escuela'),
                        defaults={
                            'nombre_escuela': esc.get('nombre_escuela')
                        }
                    )

                # Cargar calificaciones (hechos)
                calificaciones = data.get('calificaciones', [])
                for cal in calificaciones:
                    # Verificar que las FK existan
                    try:
                        estudiante = DimEstudiante.objects.get(id_estudiante=cal.get('id_estudiante'))
                        materia = DimMateria.objects.get(id_materia=cal.get('id_materia'))
                        profesor = DimProfesor.objects.get(id_profesor=cal.get('id_profesor'))
                        tiempo = DimTiempo.objects.get(id_tiempo=cal.get('id_tiempo'))
                        escuela = DimEscuela.objects.get(id_escuela=cal.get('id_escuela'))
                        
                        HechosCalificaciones.objects.update_or_create(
                            id_calificacion=cal.get('id_calificacion'),
                            defaults={
                                'id_estudiante': estudiante,
                                'id_materia': materia,
                                'id_profesor': profesor,
                                'id_tiempo': tiempo,
                                'id_escuela': escuela,
                                'calificacion': cal.get('calificacion'),
                                'puntos_obtenidos': cal.get('puntos_obtenidos'),
                                'puntos_totales': cal.get('puntos_totales'),
                            }
                        )
                    except (DimEstudiante.DoesNotExist, DimMateria.DoesNotExist, 
                            DimProfesor.DoesNotExist, DimTiempo.DoesNotExist, 
                            DimEscuela.DoesNotExist) as e:
                        return Response({"error": f"FK no encontrada: {str(e)}"}, 
                                      status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Datos cargados correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Vistas CRUD con generics para cada tabla

# DimEstudiante
class EstudianteListCreateView(generics.ListCreateAPIView):
    queryset = DimEstudiante.objects.all()
    serializer_class = DimEstudianteSerializer

class EstudianteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DimEstudiante.objects.all()
    serializer_class = DimEstudianteSerializer
    lookup_field = 'id_estudiante'

    def perform_destroy(self, instance):
        # Eliminar primero todas las calificaciones relacionadas
        HechosCalificaciones.objects.filter(id_estudiante=instance).delete()
        # Luego eliminar el estudiante
        instance.delete()

# DimMateria
class MateriaListCreateView(generics.ListCreateAPIView):
    queryset = DimMateria.objects.all()
    serializer_class = DimMateriaSerializer

class MateriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DimMateria.objects.all()
    serializer_class = DimMateriaSerializer
    lookup_field = 'id_materia'

# DimProfesor
class ProfesorListCreateView(generics.ListCreateAPIView):
    queryset = DimProfesor.objects.all()
    serializer_class = DimProfesorSerializer

class ProfesorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DimProfesor.objects.all()
    serializer_class = DimProfesorSerializer
    lookup_field = 'id_profesor'

# DimTiempo
class TiempoListCreateView(generics.ListCreateAPIView):
    queryset = DimTiempo.objects.all()
    serializer_class = DimTiempoSerializer

class TiempoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DimTiempo.objects.all()
    serializer_class = DimTiempoSerializer
    lookup_field = 'id_tiempo'

# DimEscuela
class EscuelaListCreateView(generics.ListCreateAPIView):
    queryset = DimEscuela.objects.all()
    serializer_class = DimEscuelaSerializer

class EscuelaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DimEscuela.objects.all()
    serializer_class = DimEscuelaSerializer
    lookup_field = 'id_escuela'

# HechosCalificaciones
class CalificacionListCreateView(generics.ListCreateAPIView):
    queryset = HechosCalificaciones.objects.all()
    serializer_class = HechosCalificacionesSerializer

class CalificacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HechosCalificaciones.objects.all()
    serializer_class = HechosCalificacionesSerializer
    lookup_field = 'id_calificacion'