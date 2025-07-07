-- Tabla de estudiantes
CREATE TABLE dim_estudiante (
    id_estudiante SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    carrera VARCHAR(100),
    semestre INT,
    CONSTRAINT unique_estudiante UNIQUE (nombre, apellido, carrera)
);

-- Tabla de materias
CREATE TABLE dim_materia (
    id_materia SERIAL PRIMARY KEY,
    nombre_materia VARCHAR(100),
    codigo_materia VARCHAR(20),
    creditos INT,
    departamento VARCHAR(100),
    CONSTRAINT unique_materia UNIQUE (nombre_materia, departamento)
);

-- Tabla de profesores
CREATE TABLE dim_profesor (
    id_profesor SERIAL PRIMARY KEY,
    nombre_profesor VARCHAR(100),
    apellido_profesor VARCHAR(100),
    departamento VARCHAR(100),
    CONSTRAINT unique_profesor UNIQUE (nombre_profesor, apellido_profesor, departamento)
);

-- Tabla de tiempo
CREATE TABLE dim_tiempo (
    id_tiempo SERIAL PRIMARY KEY,
    fecha DATE,
    mes VARCHAR(20),
    semestre VARCHAR(20),
    anio INT,
    periodo_academico VARCHAR(50),
    CONSTRAINT unique_fecha UNIQUE (fecha)
);

-- Tabla de escuelas
CREATE TABLE dim_escuela (
    id_escuela SERIAL PRIMARY KEY,
    nombre_escuela VARCHAR(100),
    CONSTRAINT unique_escuela UNIQUE (nombre_escuela)
);

-- Tabla de hechos (calificaciones)
CREATE TABLE hechos_calificaciones (
    id_calificacion SERIAL PRIMARY KEY,
    id_estudiante INT REFERENCES dim_estudiante(id_estudiante),
    id_materia INT REFERENCES dim_materia(id_materia),
    id_profesor INT REFERENCES dim_profesor(id_profesor),
    id_tiempo INT REFERENCES dim_tiempo(id_tiempo),
    id_escuela INT REFERENCES dim_escuela(id_escuela),
    calificacion DECIMAL(5,2),
    puntos_obtenidos INT,
    puntos_totales INT,
    CONSTRAINT unique_hechos_calificaciones UNIQUE (id_estudiante, id_materia, id_tiempo)
);
