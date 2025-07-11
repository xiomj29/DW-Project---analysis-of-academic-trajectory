# Generated by Django 5.2.4 on 2025-07-03 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DimEscuela',
            fields=[
                ('id_escuela', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_escuela', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'dim_escuela',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DimEstudiante',
            fields=[
                ('id_estudiante', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido', models.CharField(blank=True, max_length=100, null=True)),
                ('carrera', models.CharField(blank=True, max_length=100, null=True)),
                ('semestre', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dim_estudiante',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DimMateria',
            fields=[
                ('id_materia', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_materia', models.CharField(blank=True, max_length=100, null=True)),
                ('codigo_materia', models.CharField(blank=True, max_length=20, null=True)),
                ('creditos', models.IntegerField(blank=True, null=True)),
                ('departamento', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'dim_materia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DimProfesor',
            fields=[
                ('id_profesor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_profesor', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido_profesor', models.CharField(blank=True, max_length=100, null=True)),
                ('departamento', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'dim_profesor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DimTiempo',
            fields=[
                ('id_tiempo', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('mes', models.CharField(blank=True, max_length=20, null=True)),
                ('semestre', models.CharField(blank=True, max_length=20, null=True)),
                ('anio', models.IntegerField(blank=True, null=True)),
                ('periodo_academico', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'dim_tiempo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HechosCalificaciones',
            fields=[
                ('id_calificacion', models.AutoField(primary_key=True, serialize=False)),
                ('calificacion', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('puntos_obtenidos', models.IntegerField(blank=True, null=True)),
                ('puntos_totales', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hechos_calificaciones',
                'managed': False,
            },
        ),
    ]
