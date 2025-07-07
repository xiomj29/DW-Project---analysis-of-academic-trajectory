import psycopg2
import random
from datetime import datetime, timedelta

# Parámetros de conexión 
conn = psycopg2.connect(
    dbname='dw_db',
    user='admin',
    password='admin123',
    host='db',
    port='5432'
)
cursor = conn.cursor()

# Datos base para insertar
materias_isc = [
    'Fundamentos de Programación', 'Algoritmos y Estructuras de Datos', 'Análisis y Diseño de Algoritmos',
    'Teoría de la Computación', 'Compiladores', 'Inteligencia Artificial', 'Paradigmas de Programación',
    'Sistemas Operativos', 'Sistemas Distribuidos', 'Redes de Computadoras', 'Aplicaciones para Comunicaciones en Red',
    'Administración de Servicios en Red', 'Análisis y Diseño de Sistemas', 'Ingeniería de Software',
    'Desarrollo de Aplicaciones Móviles Nativas', 'Tecnologías para el Desarrollo de Aplicaciones Web',
    'Bases de Datos', 'Matemáticas Discretas', 'Cálculo', 'Comunicación Oral y Escrita'
]

materias_ia = [
    'Fundamentos de Programación', 'Algoritmos y Estructuras de Datos', 'Análisis y Diseño de Algoritmos',
    'Teoría de la Computación', 'Procesamiento de Señales', 'Paradigmas de Programación', 'Visión Artificial',
    'Formulación y Evaluación de Proyectos Informáticos', 'Algoritmos Bioinspirados', 'Reconocimiento de Voz',
    'Análisis y Diseño de Sistemas', 'Ingeniería de Software para Sistemas Inteligentes', 'Tecnologías para el Desarrollo de Aplicaciones Web',
    'Bases de Datos', 'Cálculo', 'Mecánica y Electromagnetismo', 'Comunicación Oral y Escrita',
    'Fundamentos de Inteligencia Artificial', 'Aprendizaje de Máquina', 'Redes Neuronales y Aprendizaje Profundo'
]

materias_cd = [
    'Introducción a la Ciencia de Datos', 'Programación para Ciencia de Datos', 'Bases de Datos',
    'Estadística', 'Matemáticas Avanzadas para Ciencia de Datos', 'Modelado Predictivo', 'Minería de Datos',
    'Analítica Avanzada de Datos', 'Análisis y Diseño de Algoritmos', 'Desarrollo de Aplicaciones Web',
    'Cómputo de Alto Desempeño', 'Procesamiento de Lenguaje Natural', 'Big Data', 'Optativa A', 'Optativa B',
    'Optativa C', 'Optativa D', 'Metodología de la Investigación y Divulgación Científica', 'Finanzas Empresariales', 'Métodos Numéricos'
]

nombres = ['Ana', 'Luis', 'Carlos', 'María', 'Jorge', 'Lucía', 'Andrés', 'Sofía', 'Pedro', 'Valeria',
           'Diego', 'Camila', 'Fernando', 'Marta', 'Ricardo', 'Paula', 'Eduardo', 'Gabriela', 'Manuel', 'Laura']

apellidos = ['Pérez', 'Gómez', 'Ramírez', 'López', 'Hernández', 'Martínez', 'Sánchez', 'Díaz', 'Fernández', 'García']

departamentos = ['Ingeniería en Sistemas Computacionales', 'Ingeniería en Inteligencia Artificial', 'Licenciatura en Ciencia de Datos']

prof_nombres = ['Alfredo', 'Beatriz', 'Carlos', 'Daniela', 'Esteban', 'Fernanda', 'Guillermo', 'Helena',
                'Ignacio', 'Julia', 'Kevin', 'Lorena', 'Marcos', 'Natalia', 'Oscar', 'Patricia', 'Quintín', 'Rosa', 'Sergio', 'Teresa']

prof_apellidos = ['Mendoza', 'Núñez', 'Ochoa', 'Paredes', 'Quiroz', 'Rivas', 'Soto', 'Téllez', 'Urbina', 'Vega']

escuelas = ['Escuela Superior de Cómputo']

# Funciones para insertar datos

def insertar_escuelas():
    for escuela in escuelas:
        cursor.execute("INSERT INTO dim_escuela (nombre_escuela) VALUES (%s) ON CONFLICT DO NOTHING", (escuela,))
    conn.commit()

def insertar_materias():
    ya_insertadas = set()

    for lista, dep in [
        (materias_isc, 'Ingeniería en Sistemas Computacionales'),
        (materias_ia, 'Ingeniería en Inteligencia Artificial'),
        (materias_cd, 'Licenciatura en Ciencia de Datos'),
    ]:
        for mat in lista:
            if (mat, dep) in ya_insertadas:
                continue
            ya_insertadas.add((mat, dep))
            codigo = mat[:5].upper() + str(random.randint(100, 999))
            creditos = random.randint(1, 4)
            cursor.execute("""
                INSERT INTO dim_materia (nombre_materia, codigo_materia, creditos, departamento)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (nombre_materia, departamento) DO NOTHING
            """, (mat, codigo, creditos, dep))
    conn.commit()



def insertar_estudiantes():
    carreras = ['Ingeniería en Sistemas Computacionales', 'Ingeniería en Inteligencia Artificial', 'Licenciatura en Ciencia de Datos']
    for carrera in carreras:
        for _ in range(20):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            semestre = random.randint(1, 8)
            cursor.execute("""
                INSERT INTO dim_estudiante (nombre, apellido, carrera, semestre)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (nombre, apellido, carrera) DO NOTHING
            """, (nombre, apellido, carrera, semestre))
    conn.commit()


def insertar_profesores():
    for _ in range(20):
        nombre = random.choice(prof_nombres)
        apellido = random.choice(prof_apellidos)
        departamento = random.choice(departamentos)
        cursor.execute("""
            INSERT INTO dim_profesor (nombre_profesor, apellido_profesor, departamento)
            VALUES (%s, %s, %s)
            ON CONFLICT (nombre_profesor, apellido_profesor, departamento) DO NOTHING
        """, (nombre, apellido, departamento))
    conn.commit()


def insertar_tiempos():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    delta = end_date - start_date
    for i in range(delta.days + 1):
        date = start_date + timedelta(days=i)
        mes = date.strftime('%B')
        semestre = '1' if date.month <= 6 else '2'
        anio = date.year
        periodo = 'Enero-Junio' if semestre == '1' else 'Agosto-Diciembre'
        cursor.execute("""
            INSERT INTO dim_tiempo (fecha, mes, semestre, anio, periodo_academico)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (fecha) DO NOTHING
        """, (date, mes, semestre, anio, periodo))
    conn.commit()


def insertar_hechos():
    # Obtenemos todos los estudiantes junto con su carrera
    cursor.execute("SELECT id_estudiante, carrera FROM dim_estudiante")
    estudiantes = cursor.fetchall()  # Lista de tuplas (id_estudiante, carrera)

    # Organizamos materias por carrera
    cursor.execute("SELECT id_materia, departamento FROM dim_materia")
    materias_raw = cursor.fetchall()  # (id_materia, departamento)

    materias_por_carrera = {
        'Ingeniería en Sistemas Computacionales': [],
        'Ingeniería en Inteligencia Artificial': [],
        'Licenciatura en Ciencia de Datos': []
    }

    for id_materia, departamento in materias_raw:
        if departamento in materias_por_carrera:
            materias_por_carrera[departamento].append(id_materia)

    cursor.execute("SELECT id_profesor FROM dim_profesor")
    profesores = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id_tiempo FROM dim_tiempo")
    tiempos = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id_escuela FROM dim_escuela")
    escuelas_db = [row[0] for row in cursor.fetchall()]

    total_registros = 5000
    for _ in range(total_registros):
        est_id, carrera = random.choice(estudiantes)
        materias_validas = materias_por_carrera.get(carrera, [])

        if not materias_validas:
            continue  # Si no hay materias para esa carrera, lo saltamos

        mat = random.choice(materias_validas)
        prof = random.choice(profesores)
        tiempo = random.choice(tiempos)
        esc = random.choice(escuelas_db)
        calificacion = round(random.uniform(4, 10), 2)
        puntos_totales = 100
        puntos_obtenidos = int(calificacion * 10)

        try:
            cursor.execute("""
                INSERT INTO hechos_calificaciones 
                (id_estudiante, id_materia, id_profesor, id_tiempo, id_escuela, calificacion, puntos_obtenidos, puntos_totales)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (est_id, mat, prof, tiempo, esc, calificacion, puntos_obtenidos, puntos_totales))
        except Exception as e:
            print(f"Error al insertar registro: {e}")

    conn.commit()


# Función principal para ejecutar todo
def ejecutar_todo():
    insertar_escuelas()
    insertar_materias()
    insertar_estudiantes()
    insertar_profesores()
    insertar_tiempos()
    insertar_hechos()

if __name__ == "__main__":
    ejecutar_todo()
    cursor.close()
    conn.close()
    print("Datos insertados correctamente.")
