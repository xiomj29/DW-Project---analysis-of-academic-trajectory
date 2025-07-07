// Variables globales
let students = [];
let filteredStudents = [];
let currentPage = 1;
let studentsPerPage = 10;
let isEditing = false;
let currentGradesData = [];
let subjectChart = null;
let gradeDistributionChart = null;

// URLs de la API
const API_BASE = '/api/estudiantes/';
const GRADES_API = '/api/calificaciones/estudiante/';

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
    setupEventListeners();
});

// Configurar event listeners
function setupEventListeners() {
    // Formulario
    document.getElementById('studentForm').addEventListener('submit', handleFormSubmit);
    document.getElementById('updateBtn').addEventListener('click', handleUpdate);
    document.getElementById('clearBtn').addEventListener('click', clearForm);

    // Búsqueda
    document.getElementById('searchInput').addEventListener('input', handleSearch);
    document.getElementById('refreshBtn').addEventListener('click', loadStudents);
}

// Cargar estudiantes desde la API
async function loadStudents() {
    showLoading(true);
    try {
        const response = await fetch(API_BASE);
        if (!response.ok) throw new Error('Error al cargar estudiantes');

        students = await response.json();
        filteredStudents = [...students];
        currentPage = 1;
        renderTable();
        showAlert('Estudiantes cargados correctamente', 'success');
    } catch (error) {
        showAlert('Error al cargar estudiantes: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Mostrar/ocultar indicador de carga
function showLoading(show) {
    const indicator = document.getElementById('loadingIndicator');
    const table = document.getElementById('studentsTable');

    if (show) {
        indicator.classList.remove('hidden');
        table.style.display = 'none';
    } else {
        indicator.classList.add('hidden');
        table.style.display = 'table';
    }
}

// Manejar envío del formulario
async function handleFormSubmit(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const studentData = {
        nombre: formData.get('nombre'),
        apellido: formData.get('apellido'),
        carrera: formData.get('carrera'),
        semestre: parseInt(formData.get('semestre'))
    };

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentData)
        });

        if (!response.ok) throw new Error('Error al crear estudiante');

        showAlert('Estudiante creado exitosamente', 'success');
        clearForm();
        loadStudents();
    } catch (error) {
        showAlert('Error al crear estudiante: ' + error.message, 'error');
    }
}

// Manejar actualización
async function handleUpdate() {
    const studentId = document.getElementById('studentId').value;
    const formData = new FormData(document.getElementById('studentForm'));

    const studentData = {
        nombre: formData.get('nombre'),
        apellido: formData.get('apellido'),
        carrera: formData.get('carrera'),
        semestre: parseInt(formData.get('semestre'))
    };

    try {
        const response = await fetch(`${API_BASE}${studentId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentData)
        });

        if (!response.ok) throw new Error('Error al actualizar estudiante');

        showAlert('Estudiante actualizado exitosamente', 'success');
        clearForm();
        loadStudents();
    } catch (error) {
        showAlert('Error al actualizar estudiante: ' + error.message, 'error');
    }
}

// Editar estudiante
function editStudent(id) {
    const student = students.find(s => s.id_estudiante === id);
    if (!student) return;

    document.getElementById('studentId').value = student.id_estudiante;
    document.getElementById('nombre').value = student.nombre || '';
    document.getElementById('apellido').value = student.apellido || '';
    document.getElementById('carrera').value = student.carrera || '';
    document.getElementById('semestre').value = student.semestre || '';

    // Cambiar a modo edición
    document.getElementById('saveBtn').style.display = 'none';
    document.getElementById('updateBtn').style.display = 'inline-block';
    isEditing = true;
}

// Eliminar estudiante y todos sus datos relacionados
async function deleteStudent(id) {
    if (!confirm('¿Está seguro de que desea eliminar este estudiante y TODAS sus calificaciones relacionadas? Esta acción no se puede deshacer.')) return;

    try {
        const deleteResponse = await fetch(`${API_BASE}${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!deleteResponse.ok) {
            const errorData = await deleteResponse.json();
            throw new Error(errorData.detail || 'Error al eliminar estudiante');
        }

        showAlert('Estudiante y todas sus calificaciones relacionadas eliminadas exitosamente', 'success');
        loadStudents();
    } catch (error) {
        console.error('Error al eliminar:', error);
        showAlert('Error al eliminar estudiante: ' + error.message, 'error');
    }
}

// Limpiar formulario
function clearForm() {
    document.getElementById('studentForm').reset();
    document.getElementById('studentId').value = '';
    document.getElementById('saveBtn').style.display = 'inline-block';
    document.getElementById('updateBtn').style.display = 'none';
    isEditing = false;
}

// Manejar búsqueda
function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    filteredStudents = students.filter(student =>
        (student.nombre && student.nombre.toLowerCase().includes(searchTerm)) ||
        (student.apellido && student.apellido.toLowerCase().includes(searchTerm)) ||
        (student.carrera && student.carrera.toLowerCase().includes(searchTerm)) ||
        (student.id_estudiante && student.id_estudiante.toString().includes(searchTerm))
    );
    currentPage = 1;
    renderTable();
}

// Renderizar tabla
function renderTable() {
    const tbody = document.getElementById('studentsTableBody');
    const startIndex = (currentPage - 1) * studentsPerPage;
    const endIndex = startIndex + studentsPerPage;
    const currentStudents = filteredStudents.slice(startIndex, endIndex);

    tbody.innerHTML = '';

    if (currentStudents.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #666;">No se encontraron estudiantes</td></tr>';
        return;
    }

    currentStudents.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.id_estudiante}</td>
            <td>${student.nombre || 'N/A'}</td>
            <td>${student.apellido || 'N/A'}</td>
            <td>${student.carrera || 'N/A'}</td>
            <td>${student.semestre || 'N/A'}</td>
            <td class="actions">
                <button class="btn btn-warning btn-small" onclick="editStudent(${student.id_estudiante})">
                    ✏️ Editar
                </button>
                <button class="btn btn-primary btn-small" onclick="viewGrades(${student.id_estudiante})">
                    📊 Calificaciones
                </button>
                <button class="btn btn-danger btn-small" onclick="deleteStudent(${student.id_estudiante})">
                    🗑️ Eliminar
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });

    renderPagination();
}

// Renderizar paginación
function renderPagination() {
    const container = document.getElementById('paginationContainer');
    const totalPages = Math.ceil(filteredStudents.length / studentsPerPage);

    container.innerHTML = '';

    if (totalPages <= 1) return;

    // Botón anterior
    const prevBtn = document.createElement('button');
    prevBtn.textContent = '« Anterior';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    };
    container.appendChild(prevBtn);

    // Botones de página
    for (let i = 1; i <= totalPages; i++) {
        const pageBtn = document.createElement('button');
        pageBtn.textContent = i;
        pageBtn.className = currentPage === i ? 'active' : '';
        pageBtn.onclick = () => {
            currentPage = i;
            renderTable();
        };
        container.appendChild(pageBtn);
    }

    // Botón siguiente
    const nextBtn = document.createElement('button');
    nextBtn.textContent = 'Siguiente »';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    };
    container.appendChild(nextBtn);
}

// Mostrar alertas
function showAlert(message, type = 'info') {
    const container = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    container.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Ver calificaciones de un estudiante
async function viewGrades(studentId) {
    try {
        // Obtener datos del estudiante
        const student = students.find(s => s.id_estudiante === studentId);
        if (!student) {
            showAlert('Estudiante no encontrado', 'error');
            return;
        }

        // Obtener calificaciones
        const response = await fetch(`${GRADES_API}${studentId}/`);
        if (!response.ok) {
            throw new Error('El alumno no tiene calificaciones registradas. Importante: No se pueden registrar datos');
        }

        currentGradesData = await response.json();

        // Mostrar modal con los datos
        showGradesModal(student, currentGradesData);

    } catch (error) {
        console.error('Error al cargar calificaciones:', error);
        showAlert('Error al cargar calificaciones: ' + error.message, 'error');
    }
}

// Mostrar modal de calificaciones
function showGradesModal(student, grades) {
    // Actualizar información del estudiante
    const studentInfo = document.getElementById('studentInfo');
    studentInfo.innerHTML = `
        <h3>Información del Estudiante</h3>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Nombre Completo</div>
                <div class="info-value">${student.nombre || 'N/A'} ${student.apellido || 'N/A'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">ID Estudiante</div>
                <div class="info-value">${student.id_estudiante}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Carrera</div>
                <div class="info-value">${student.carrera || 'N/A'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Semestre</div>
                <div class="info-value">${student.semestre || 'N/A'}</div>
            </div>
        </div>
    `;

    if (grades.length === 0) {
        document.getElementById('statsSummary').innerHTML = '<div class="no-data">No hay calificaciones registradas para este estudiante.</div>';
        document.getElementById('gradesGrid').innerHTML = '<div class="no-data">No hay calificaciones para mostrar.</div>';
        document.getElementById('gradesModal').style.display = 'block';
        return;
    }

    // Calcular estadísticas
    const stats = calculateStats(grades);
    updateStatsSummary(stats);

    // Actualizar grid de calificaciones
    updateGradesGrid(grades);

    // Crear gráficos
    createCharts(grades);

    // Mostrar modal
    document.getElementById('gradesModal').style.display = 'block';
}

// Calcular estadísticas
function calculateStats(grades) {
    const validGrades = grades.filter(g => g.calificacion !== null);
    const totalGrades = validGrades.length;

    if (totalGrades === 0) {
        return {
            totalSubjects: 0,
            averageGrade: 0,
            highestGrade: 0,
            lowestGrade: 0,
            passedSubjects: 0,
            failedSubjects: 0
        };
    }

    const gradeValues = validGrades.map(g => parseFloat(g.calificacion));
    const averageGrade = gradeValues.reduce((a, b) => a + b, 0) / totalGrades;
    const highestGrade = Math.max(...gradeValues);
    const lowestGrade = Math.min(...gradeValues);
    const passedSubjects = gradeValues.filter(g => g >= 6).length;
    const failedSubjects = totalGrades - passedSubjects;

    return {
        totalSubjects: totalGrades,
        averageGrade: averageGrade.toFixed(2),
        highestGrade: highestGrade.toFixed(2),
        lowestGrade: lowestGrade.toFixed(2),
        passedSubjects,
        failedSubjects
    };
}

// Actualizar resumen estadístico
function updateStatsSummary(stats) {
    const container = document.getElementById('statsSummary');
    container.innerHTML = `
        <div class="stat-card">
            <div class="stat-number">${stats.totalSubjects}</div>
            <div class="stat-label">Materias Cursadas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${stats.averageGrade}</div>
            <div class="stat-label">Promedio General</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${stats.highestGrade}</div>
            <div class="stat-label">Calificación Máxima</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${stats.lowestGrade}</div>
            <div class="stat-label">Calificación Mínima</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${stats.passedSubjects}</div>
            <div class="stat-label">Materias Aprobadas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${stats.failedSubjects}</div>
            <div class="stat-label">Materias Reprobadas</div>
        </div>
    `;
}

// Actualizar grid de calificaciones con botón de eliminar
function updateGradesGrid(grades) {
    const container = document.getElementById('gradesGrid');
    container.innerHTML = '';

    grades.forEach(grade => {
        const gradeValue = parseFloat(grade.calificacion) || 0;
        const gradeClass = getGradeClass(gradeValue);

        const card = document.createElement('div');
        card.className = 'grade-card';
        card.innerHTML = `
            <div class="grade-header">
                <div class="subject-name">${grade.id_materia?.nombre_materia || 'N/A'}</div>
                <div class="grade-score ${gradeClass}">${gradeValue.toFixed(1)}</div>
            </div>
            <div class="grade-details">
                <div><strong>Código:</strong> ${grade.id_materia?.codigo_materia || 'N/A'}</div>
                <div><strong>Créditos:</strong> ${grade.id_materia?.creditos || 'N/A'}</div>
                <div><strong>Profesor:</strong> ${grade.id_profesor?.nombre_profesor || 'N/A'} ${grade.id_profesor?.apellido_profesor || ''}</div>
                <div><strong>Período:</strong> ${grade.id_tiempo?.periodo_academico || 'N/A'}</div>
                <div><strong>Puntos:</strong> ${grade.puntos_obtenidos || 0}/${grade.puntos_totales || 0}</div>
                <div><strong>Departamento:</strong> ${grade.id_materia?.departamento || 'N/A'}</div>
            </div>
        `;
        container.appendChild(card);
    });
}

// Obtener clase CSS según la calificación
function getGradeClass(grade) {
    if (grade >= 9) return 'grade-excellent';
    if (grade >= 8) return 'grade-good';
    if (grade >= 6) return 'grade-regular';
    return 'grade-poor';
}

// Crear gráficos
function createCharts(grades) {
    createGradeDistributionChart(grades);
}

// Crear gráfico de distribución de calificaciones
function createGradeDistributionChart(grades) {
    const ctx = document.getElementById('gradeDistributionChart').getContext('2d');

    if (gradeDistributionChart) gradeDistributionChart.destroy();

    const validGrades = grades.filter(g => g.calificacion !== null);
    const gradeValues = validGrades.map(g => parseFloat(g.calificacion));

    const ranges = {
        'Excelente (9-10)': gradeValues.filter(g => g >= 9).length,
        'Bueno (8-8.9)': gradeValues.filter(g => g >= 8 && g < 9).length,
        'Regular (6-7.9)': gradeValues.filter(g => g >= 6 && g < 8).length,
        'Reprobado (0-5.9)': gradeValues.filter(g => g < 6).length
    };

    gradeDistributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(ranges),
            datasets: [{
                data: Object.values(ranges),
                backgroundColor: ['#27ae60', '#3498db', '#f39c12', '#e74c3c'],
                borderWidth: 1,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    align: 'center',
                    labels: {
                        boxWidth: 12,
                        padding: 10,
                        font: {
                            size: 11
                        }
                    }
                }
            },
            cutout: '40%'
        }
    });
}

// Obtener color según la calificación
function getGradeColor(grade) {
    if (grade >= 9) return '#27ae60';
    if (grade >= 8) return '#3498db';
    if (grade >= 6) return '#f39c12';
    return '#e74c3c';
}

// Cerrar modal de calificaciones
function closeGradesModal() {
    document.getElementById('gradesModal').style.display = 'none';

    // Limpiar gráficos
    if (subjectChart) {
        subjectChart.destroy();
        subjectChart = null;
    }
    if (gradeDistributionChart) {
        gradeDistributionChart.destroy();
        gradeDistributionChart = null;
    }
}

// Cerrar modal al hacer clic fuera de él
window.onclick = function(event) {
    const modal = document.getElementById('gradesModal');
    if (event.target === modal) {
        closeGradesModal();
    }
}