# dw_project/urls.py
from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse
from django.views.generic import TemplateView

def api_root(request):
    return JsonResponse({
        'message': 'API del Data Warehouse de Calificaciones',
        'endpoints': {
            'estudiantes': '/api/estudiantes/',
            'materias': '/api/materias/',
            'profesores': '/api/profesores/',
            'tiempos': '/api/tiempos/',
            'escuelas': '/api/escuelas/',
            'calificaciones': '/api/calificaciones/',
            'calificaciones_por_estudiante': '/api/calificaciones/estudiante/<id>/',
            'carga_masiva': '/api/load-data/',
        }
    })

class IndexView(TemplateView):
    template_name = 'warehouse/index.html'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('api/', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('', include('warehouse.urls')),
]