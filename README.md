
# Sistema de Análisis Académico con Data Warehouse

Este proyecto es un sistema para el análisis del rendimiento académico de estudiantes universitarios, utilizando un Data Warehouse implementado con Django y PostgreSQL.

---

## Tabla de Contenido

- [Descripción General](#descripción-general)  
- [Características](#características)  
- [Tecnologías Usadas](#tecnologías-usadas)  
- [Estructura del Proyecto](#estructura-del-proyecto)  
- [Instalación y Ejecución](#instalación-y-ejecución)  
- [Modelo de Datos](#modelo-de-datos)  
- [Generación de Datos Sintéticos](#generación-de-datos-sintéticos)  
- [API REST](#api-rest)  
- [Autor](#autor)  

---

## Descripción General

Este sistema simula un entorno académico en el que se almacenan y analizan las calificaciones de estudiantes en diversas materias, considerando profesores, escuelas y períodos de tiempo. La base de datos está organizada en un esquema dimensional para facilitar análisis posteriores.

Se incluye un script para generar datos sintéticos, evitando duplicados y manteniendo coherencia entre carreras y materias.

---

## Características

- Modelo dimensional con tablas de dimensiones: estudiantes, materias, profesores, tiempo y escuelas.  
- Tabla de hechos con calificaciones y puntos obtenidos.  
- Restricciones de unicidad para evitar registros duplicados.  
- Script en Python para generación automática y segura de datos sintéticos.  
- API REST para gestión y consulta de datos (por implementar o extender).  

---

## Tecnologías Usadas

- Python 3.x  
- Django >= 5.2  
- Django REST Framework  
- PostgreSQL  
- psycopg2-binary  

---

## Estructura del Proyecto

```
dw_project/
├── dw_project/              # Configuración del proyecto
├── fontend/                 # Código html, css y js
├── warehouse/               # Código Django
├── scripts/                 # Scripts para generación y limpieza de datos
│   └── insert_data.py
├── Dockerfile               # Opcional para contenerización
├── docker-compose.yml       # Para levantar servicios con Docker o Podman
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación (este archivo)
```

---

## Instalación y Ejecución

### Requisitos Previos

- Tener instalado Docker o Podman en el sistema.
- Python 3.x (para ejecutar scripts adicionales).
- PostgreSQL configurado (se usa dentro del contenedor).

### Pasos para levantar el sistema

1. Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd dw_project
```

2. Levanta los contenedores con Docker o Podman:

Con **Docker**:

```bash
docker-compose up -d
```

Con **Podman**:

```bash
podman-compose up -d
```

3. Verifica que los contenedores estén activos:

```bash
docker ps
# o
podman ps
```

4. Para detener los contenedores:

```bash
docker-compose down
# o
podman-compose down
```

---

## Modelo de Datos

El esquema está organizado en tablas dimensionales y una tabla de hechos con las siguientes características:

### Tablas Dimensionales

- **dim_estudiante**  
  - id_estudiante (PK)  
  - nombre  
  - apellido  
  - carrera  
  - semestre  
  - **Restricción:** combinación única de (nombre, apellido, carrera)

- **dim_materia**  
  - id_materia (PK)  
  - nombre_materia  
  - codigo_materia  
  - creditos  
  - departamento  
  - **Restricción:** combinación única de (nombre_materia, departamento)

- **dim_profesor**  
  - id_profesor (PK)  
  - nombre_profesor  
  - apellido_profesor  
  - departamento  
  - **Restricción:** combinación única de (nombre_profesor, apellido_profesor, departamento)

- **dim_tiempo**  
  - id_tiempo (PK)  
  - fecha  
  - mes  
  - semestre  
  - anio  
  - periodo_academico  
  - **Restricción:** fecha única (único registro por día)

- **dim_escuela**  
  - id_escuela (PK)  
  - nombre_escuela  
  - **Restricción:** nombre_escuela único

### Tabla de Hechos

- **hechos_calificaciones**  
  - id_calificacion (PK)  
  - id_estudiante (FK)  
  - id_materia (FK)  
  - id_profesor (FK)  
  - id_tiempo (FK)  
  - id_escuela (FK)  
  - calificacion (decimal)  
  - puntos_obtenidos (int)  
  - puntos_totales (int)  
  - **Restricción:** combinación única de (id_estudiante, id_materia, id_tiempo) para evitar duplicados en calificaciones por estudiante, materia y fecha.

Estas restricciones UNIQUE garantizan la integridad y evitan registros duplicados en el Data Warehouse.

---

## Generación de Datos Sintéticos

Incluye un script en Python `insert_data.py` ubicado en la carpeta `scripts/` que:

- Inserta datos en las tablas dimensionales respetando las restricciones.
- Genera calificaciones y registros de hechos coherentes con las carreras y materias.
- Evita la inserción duplicada usando las restricciones UNIQUE.
- Se conecta a la base de datos PostgreSQL para hacer inserciones.

Ejecuta el script desde la terminal:

```bash
python scripts/insert_data.py
```

Asegúrate de configurar correctamente los parámetros de conexión en el script (`host`, `user`, `password`, `dbname`).

---

## API REST

El proyecto cuenta con una API REST para:

- Cargar y modificar datos (excluyendo calificaciones, por ahora) 
- Consultar análisis académicos  
- Actualizar dimensiones  

Se recomienda usar Django REST Framework para la implementación de endpoints.

---

## Autor

- **Danna Xiomara Montes Jaimes**
---

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---


