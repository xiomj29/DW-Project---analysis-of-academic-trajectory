# warehouse/urls.py
from django.urls import path
from .views import (
    EstudianteListCreateView, EstudianteDetailView,
    MateriaListCreateView, MateriaDetailView,
    ProfesorListCreateView, ProfesorDetailView,
    TiempoListCreateView, TiempoDetailView,
    EscuelaListCreateView, EscuelaDetailView,
    CalificacionListCreateView, CalificacionDetailView, 
    LoadDataView, CalificacionesEstudianteView
)

urlpatterns = [
    # API específica para calificaciones por estudiante
    path('api/calificaciones/estudiante/<int:id_estudiante>/', 
         CalificacionesEstudianteView.as_view(), name='calificaciones_estudiante'),
    
    # API para carga masiva de datos
    path('api/load-data/', LoadDataView.as_view(), name='load-data'),
    
    # Estudiantes
    path('api/estudiantes/', EstudianteListCreateView.as_view(), name='estudiantes-list-create'),
    path('api/estudiantes/<int:id_estudiante>/', EstudianteDetailView.as_view(), name='estudiantes-detail'),

    # Materias
    path('api/materias/', MateriaListCreateView.as_view(), name='materias-list-create'),
    path('api/materias/<int:id_materia>/', MateriaDetailView.as_view(), name='materias-detail'),

    # Profesores
    path('api/profesores/', ProfesorListCreateView.as_view(), name='profesores-list-create'),
    path('api/profesores/<int:id_profesor>/', ProfesorDetailView.as_view(), name='profesores-detail'),

    # Tiempo
    path('api/tiempos/', TiempoListCreateView.as_view(), name='tiempos-list-create'),
    path('api/tiempos/<int:id_tiempo>/', TiempoDetailView.as_view(), name='tiempos-detail'),

    # Escuela
    path('api/escuelas/', EscuelaListCreateView.as_view(), name='escuelas-list-create'),
    path('api/escuelas/<int:id_escuela>/', EscuelaDetailView.as_view(), name='escuelas-detail'),

    # Calificaciones
    path('api/calificaciones/', CalificacionListCreateView.as_view(), name='calificaciones-list-create'),
    path('api/calificaciones/<int:id_calificacion>/', CalificacionDetailView.as_view(), name='calificaciones-detail'),
]