from backend.admin import AdminOperations
from tabulate import tabulate

class AdminUI:
    def __init__(self, user):
        self.user = user
        self.operations = AdminOperations() 
        
    def show_menu(self):
        while True:
            print("\n=== MENÚ ADMINISTRADOR ===")
            print("1. Gestión de Estudiantes")
            print("2. Gestión de Profesores")
            print("3. Gestión de Cursos")
            print("4. Reportes")
            print("5. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._gestion_estudiantes()
            elif opcion == "2":
                self._gestion_profesores()
            elif opcion == "3":
                self._gestion_cursos()
            elif opcion == "4":
                self._reportes()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida")
                
    def _gestion_cursos(self):
        while True:
            print("\n=== GESTIÓN DE CURSOS ===")
            print("1. Listar cursos")
            print("2. Agregar curso")
            print("3. Asignar estudiantes a curso")
            print("4. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._listar_cursos()
            elif opcion == "2":
                self._agregar_curso()
            elif opcion == "3":
                self._asignar_estudiantes_curso()
            elif opcion == "4":
                break
            else:
                print("Opción no válida")
                
    def _listar_cursos(self):
        try:
            cursos = self.operations.listar_cursos()
            if not cursos:
                print("No hay cursos registrados")
                return

            print("\n=== LISTADO COMPLETO DE CURSOS ===")
            print(tabulate(
                [
                    (
                        c['id_curso'],
                        c.get('nombre_curso', 'Sin nombre'),
                        c.get('nombre_profesor', 'Sin profesor'),
                        c.get('nombre_categoria', 'Sin categoría'),
                        c.get('fecha_inicio', 'Sin fecha'),
                        c.get('fecha_fin', 'Sin fecha'),
                        f"${c.get('precio', 0):,}"
                    )
                    for c in cursos
                ],
                headers=[
                    'ID', 'Curso', 'Profesor', 
                    'Categoría', 'Inicio', 'Fin', 'Precio'
                ],
                tablefmt='grid'
            ))
        except Exception as e:
            print(f"❌ Error al cargar los cursos: {str(e)}")
        finally:
            input("\nPresione Enter para continuar...")

    def _asignar_estudiantes_curso(self):
        print("\n=== ASIGNAR ESTUDIANTES A CURSO ===")
        
        try:
            # Obtener lista de cursos con nombres consistentes
            cursos = self.operations.listar_cursos()
            if not cursos:
                print("No hay cursos disponibles para asignación")
                return

            print("\nCursos disponibles:")
            print(tabulate(
                [
                    (c['id_curso'], 
                    c.get('nombre_curso', 'Sin nombre'),  # Usamos get() con valor por defecto
                    c.get('nombre_profesor', 'Sin profesor'),
                    c.get('nombre_categoria', 'Sin categoría'))
                    for c in cursos
                ],
                headers=['ID', 'Nombre del Curso', 'Profesor', 'Categoría'],
                tablefmt='grid'
            ))

            id_curso = int(input("\nIngrese el ID del curso: "))
            
            # Verificar que el curso existe
            curso_seleccionado = next((c for c in cursos if c['id_curso'] == id_curso), None)
            if not curso_seleccionado:
                print("❌ Error: El ID del curso no existe")
                return

            # Obtener estudiantes no matriculados
            estudiantes = self.operations.listar_estudiantes_no_matriculados(id_curso)
            if not estudiantes:
                print("Todos los estudiantes ya están matriculados en este curso")
                return

            print("\nEstudiantes disponibles para asignar:")
            print(tabulate(
                [
                    (e['id_estudiante'], 
                    e.get('nombre_estudiante', 'Sin nombre'), 
                    e.get('email', 'Sin email'))
                    for e in estudiantes
                ],
                headers=['ID', 'Nombre del Estudiante', 'Email'],
                tablefmt='grid'
            ))

            id_estudiante = int(input("\nIngrese el ID del estudiante: "))
            
            # Verificar que el estudiante existe
            estudiante_seleccionado = next((e for e in estudiantes if e['id_estudiante'] == id_estudiante), None)
            if not estudiante_seleccionado:
                print("❌ Error: El ID del estudiante no es válido")
                return

            # Asignar estudiante al curso
            if self.operations.asignar_estudiante_curso(id_estudiante, id_curso):
                print(f"\n✅ Estudiante {estudiante_seleccionado.get('nombre_estudiante', '')} asignado exitosamente al curso {curso_seleccionado.get('nombre_curso', '')}")
            else:
                print("❌ No se pudo completar la asignación")

        except ValueError:
            print("❌ Error: Debe ingresar un número válido para los IDs")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
        finally:
            input("\nPresione Enter para volver al menú...")

    """def _ver_estudiantes_curso(self):
        print("\n=== ESTUDIANTES POR CURSO ===")
        
        cursos = self.operations.listar_cursos()
        if not cursos:
            print("No hay cursos registrados")
            return
            
        print("\nCursos disponibles:")
        print(tabulate(
            [(c['id_curso'], c['nombre']) for c in cursos],
            headers=['ID', 'Nombre del Curso'],
            tablefmt='grid'
        ))
        
        try:
            id_curso = int(input("\nID del curso para ver estudiantes: "))
            estudiantes = self.operations.listar_estudiantes_curso(id_curso)
            
            if estudiantes:
                print("\nEstudiantes matriculados:")
                print(tabulate(
                    [(e['id_estudiante'], e['nombre'], e['email']) for e in estudiantes],
                    headers=['ID', 'Nombre', 'Email'],
                    tablefmt='grid'
                ))
            else:
                print("No hay estudiantes matriculados en este curso")
                
        except ValueError:
            print("❌ El ID del curso debe ser un número")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")"""
            
    def _agregar_curso(self):
        print("\n=== NUEVO CURSO ===")
        
        try:
            # 1. Mostrar profesores disponibles primero
            profesores = self.operations.listar_profesores()
            if not profesores:
                print("No hay profesores registrados. Debe registrar profesores primero.")
                input("\nPresione Enter para volver...")
                return
            
            print("\nProfesores disponibles:")
            print(tabulate(
                [(p['id_profesor'], p['nombre'], 
                p.get('area_principal', 'N/A'),
                p.get('email', '')) 
                for p in profesores],
                headers=['ID', 'Nombre', 'Área Principal', 'Email'],
                tablefmt='grid'
            ))
            
            # 2. Mostrar categorías disponibles
            categorias = self.operations.listar_categorias()
            if not categorias:
                print("No hay categorías registradas. Debe registrar categorías primero.")
                input("\nPresione Enter para volver...")
                return
            
            print("\nCategorías disponibles:")
            print(tabulate(
                [(c['id_categoria'], c['nombre']) for c in categorias],
                headers=['ID', 'Nombre'],
                tablefmt='grid'
            ))
            
            # 3. Recolectar datos del curso después de mostrar las tablas
            datos = {
                'id_profesor': int(input("\nID del profesor: ")),
                'nombre': input("Nombre del curso: ").strip(),
                'id_categoria': int(input("ID de categoría: ")),
                'url_contenido': input("URL de contenido: ").strip(),
                'periodo': self._validar_periodo(),
                'precio': float(input("Precio: ")),
                'año': int(input("Año: ")),
                'fecha_inicio': self._validar_fecha("Fecha inicio (YYYY-MM-DD): "),
                'fecha_fin': self._validar_fecha("Fecha fin (YYYY-MM-DD): ")
            }
            
            # Validar que el profesor existe
            if not any(p['id_profesor'] == datos['id_profesor'] for p in profesores):
                print("❌ El ID del profesor no existe")
                input("\nPresione Enter para volver...")
                return
                
            # Validar que la categoría existe
            if not any(c['id_categoria'] == datos['id_categoria'] for c in categorias):
                print("❌ El ID de categoría no existe")
                input("\nPresione Enter para volver...")
                return
                
            # Insertar curso
            if self.operations.insertar_curso(**datos):
                print("\n✅ Curso registrado exitosamente")
                # Mostrar el curso recién creado
                nuevo_curso = self.operations.obtener_ultimo_curso_creado()
                if nuevo_curso:
                    print("\nCurso creado:")
                    print(tabulate(
                        [(nuevo_curso['id_curso'], nuevo_curso['nombre_curso'])],
                        headers=['ID', 'Nombre'],
                        tablefmt='grid'
                    ))
            else:
                print("❌ Error al registrar el curso")
                
        except ValueError as e:
            print(f"❌ Error en los datos ingresados: {str(e)}")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
        finally:
            input("\nPresione Enter para volver al menú...")
            
            
    def _validar_periodo(self):
        while True:
            periodo = input("Periodo (1/2): ")
            if periodo in ['1', '2']:
                return int(periodo)
            print("❌ Error: El período debe ser 1 o 2")

    def _validar_fecha(self, mensaje):
        while True:
            fecha = input(mensaje)
            try:
                # Validación básica de formato de fecha
                if len(fecha) == 10 and fecha[4] == '-' and fecha[7] == '-':
                    year, month, day = map(int, fecha.split('-'))
                    if 1 <= month <= 12 and 1 <= day <= 31:  # Validación muy básica
                        return fecha
            except ValueError:
                pass
            print("❌ Formato de fecha inválido. Use YYYY-MM-DD (ej: 2023-12-31)")
        
    def _gestion_estudiantes(self):
           while True:
            print("\n=== GESTIÓN DE ESTUDIANTES ===")
            print("1. Listar estudiantes")
            print("2. Agregar estudiante")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                estudiantes = self.operations.listar_estudiantes()
                if estudiantes:
                    print(tabulate(estudiantes, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay estudiantes registrados")
            elif opcion == "2":
                self._agregar_estudiante()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")
                
    def _listar_estudiantes(self):
        try:
            return self.db.execute_query("SELECT id_estudiante, id_nodo, nombre, email, genero FROM estudiante")
        finally:
            self.db.close()

    def _agregar_estudiante(self):
        print("\n=== NUEVO ESTUDIANTE ===")
        datos = {
            'id_estudiante': input("ID: "),
            'id_nodo': input("ID de nodo: "),
            'nombre': input("Nombre completo: "),
            'email': input("Email: "),
            'genero': self._validar_genero(),
            'contrasena': input("Contraseña: ")
        }
        
        if self.operations.insertar_estudiante(**datos):
            print("✅ Estudiante registrado exitosamente")

    def _gestion_profesores(self):
        while True:
            print("\n=== GESTIÓN DE PROFESORES ===")
            print("1. Listar profesores")
            print("2. Agregar profesor")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                profesores = self.operations.listar_profesores()
                if profesores:
                    print(tabulate(profesores, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay profesores registrados")
            elif opcion == "2":
                self._agregar_profesor()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _agregar_profesor(self):
        print("\n=== NUEVO PROFESOR ===")
        datos = {
            'id_profesor': input("ID: "),
            'nombre': input("Nombre completo: "),
            'email': input("Email: "),
            'genero': self._validar_genero(),
            'area_principal': input("Área principal: "),
            'area_alternativa': input("Área alternativa (opcional): "),
            'contrasena': input("Contraseña: ")
        }
        
        if self.operations.insertar_profesor(**datos):
            print("✅ Profesor registrado exitosamente")

    
    def _reportes(self):
        while True:
            print("\n=== REPORTES ===")
            print("1. Listar todos los usuarios")
            print("2. Ver detalles completos de un curso")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                usuarios = self.operations.listar_todos_usuarios()
                if usuarios:
                    print(tabulate(usuarios, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay usuarios registrados")
            elif opcion == "2":
                self._ver_detalles_curso()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _ver_detalles_curso(self):
        print("\n=== DETALLES COMPLETOS DE CURSO ===")
        
        try:
            # Obtener lista de cursos
            cursos = self.operations.listar_cursos()
            if not cursos:
                print("No hay cursos registrados")
                return

            print("\nCursos disponibles:")
            print(tabulate(
                [(c['id_curso'], c.get('nombre_curso', 'Sin nombre')) for c in cursos],
                headers=['ID', 'Nombre del Curso'],
                tablefmt='grid'
            ))
            
            id_curso = int(input("\nIngrese el ID del curso a consultar: "))
            
            # Buscar el curso seleccionado
            curso = next((c for c in cursos if c['id_curso'] == id_curso), None)
            if not curso:
                print("❌ Error: El ID del curso no existe")
                return

            # Obtener información detallada del curso
            print("\n=== INFORMACIÓN DEL CURSO ===")
            print(tabulate(
                [
                    ('ID', curso['id_curso']),
                    ('Nombre', curso.get('nombre_curso', 'Sin nombre')),
                    ('Profesor', curso.get('nombre_profesor', 'Sin profesor')),
                    ('Categoría', curso.get('nombre_categoria', 'Sin categoría')),
                    ('URL Contenido', curso.get('url_contenido', 'No disponible')),
                    ('Período', curso.get('periodo', 'No disponible')),
                    ('Precio', f"${curso.get('precio', 0):,}"),
                    ('Año', curso.get('año', 'No disponible')),
                    ('Fecha Inicio', curso.get('fecha_inicio', 'No disponible')),
                    ('Fecha Fin', curso.get('fecha_fin', 'No disponible'))
                ],
                tablefmt='grid'
            ))

            # Obtener información del profesor
            profesor = self._obtener_profesor(curso.get('id_profesor', None))
            if profesor:
                print("\n=== INFORMACIÓN DEL PROFESOR ===")
                print(tabulate(
                    [
                        ('ID', profesor['id_profesor']),
                        ('Nombre', profesor['nombre']),
                        ('Email', profesor.get('email', 'No disponible')),
                        ('Género', profesor.get('genero', 'No disponible')),
                        ('Área Principal', profesor.get('area_principal', 'No disponible')),
                        ('Área Alternativa', profesor.get('area_alternativa', 'No disponible'))
                    ],
                    tablefmt='grid'
                ))

            # Obtener estudiantes matriculados
            estudiantes = self.operations.listar_estudiantes_curso(id_curso)
            if estudiantes:
                print("\n=== ESTUDIANTES MATRICULADOS ===")
                print(tabulate(
                    [(e['id_estudiante'], e['nombre'], e['email']) for e in estudiantes],
                    headers=['ID', 'Nombre', 'Email'],
                    tablefmt='grid'
                ))
            else:
                print("\nNo hay estudiantes matriculados en este curso")

        except ValueError:
            print("❌ Error: Debe ingresar un número válido para el ID del curso")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
        finally:
            input("\nPresione Enter para volver al menú...")

    def _obtener_profesor(self, id_profesor):
        """Obtiene los detalles completos de un profesor"""
        if not id_profesor:
            return None
            
        try:
            # Necesitaríamos agregar este método en AdminOperations
            profesores = self.operations.listar_profesores()
            return next((p for p in profesores if p['id_profesor'] == id_profesor), None)
        except Exception:
            return None
        
    def _reportes(self):
        while True:
            print("\n=== REPORTES ===")
            print("1. Listar todos los usuarios")
            print("2. Ver detalles completos de un curso")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                usuarios = self.operations.listar_todos_usuarios()
                if usuarios:
                    print(tabulate(usuarios, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay usuarios registrados")
            elif opcion == "2":
                self._ver_detalles_curso()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _ver_detalles_curso(self):
        print("\n=== DETALLES COMPLETOS DE CURSO ===")
        
        try:
            # Obtener lista de cursos
            cursos = self.operations.listar_cursos()
            if not cursos:
                print("No hay cursos registrados")
                return

            print("\nCursos disponibles:")
            print(tabulate(
                [(c['id_curso'], c.get('nombre_curso', 'Sin nombre')) for c in cursos],
                headers=['ID', 'Nombre del Curso'],
                tablefmt='grid'
            ))
            
            id_curso = int(input("\nIngrese el ID del curso a consultar: "))
            
            # Buscar el curso seleccionado
            curso = next((c for c in cursos if c['id_curso'] == id_curso), None)
            if not curso:
                print("❌ Error: El ID del curso no existe")
                return

            # Obtener información detallada del curso
            print("\n=== INFORMACIÓN DEL CURSO ===")
            print(tabulate(
                [
                    ('ID', curso['id_curso']),
                    ('Nombre', curso.get('nombre_curso', 'Sin nombre')),
                    ('Profesor', curso.get('nombre_profesor', 'Sin profesor')),
                    ('Categoría', curso.get('nombre_categoria', 'Sin categoría')),
                    ('URL Contenido', curso.get('url_contenido', 'No disponible')),
                    ('Período', curso.get('periodo', 'No disponible')),
                    ('Precio', f"${curso.get('precio', 0):,}"),
                    ('Año', curso.get('año', 'No disponible')),
                    ('Fecha Inicio', curso.get('fecha_inicio', 'No disponible')),
                    ('Fecha Fin', curso.get('fecha_fin', 'No disponible'))
                ],
                tablefmt='grid'
            ))

            # Obtener información del profesor
            profesor = self._obtener_profesor(curso.get('id_profesor', None))
            if profesor:
                print("\n=== INFORMACIÓN DEL PROFESOR ===")
                print(tabulate(
                    [
                        ('ID', profesor['id_profesor']),
                        ('Nombre', profesor['nombre']),
                        ('Email', profesor.get('email', 'No disponible')),
                        ('Género', profesor.get('genero', 'No disponible')),
                        ('Área Principal', profesor.get('area_principal', 'No disponible')),
                        ('Área Alternativa', profesor.get('area_alternativa', 'No disponible'))
                    ],
                    tablefmt='grid'
                ))

            # Obtener estudiantes matriculados
            estudiantes = self.operations.listar_estudiantes_curso(id_curso)
            if estudiantes:
                print("\n=== ESTUDIANTES MATRICULADOS ===")
                print(tabulate(
                    [(e['id_estudiante'], e['nombre'], e['email']) for e in estudiantes],
                    headers=['ID', 'Nombre', 'Email'],
                    tablefmt='grid'
                ))
            else:
                print("\nNo hay estudiantes matriculados en este curso")

        except ValueError:
            print("❌ Error: Debe ingresar un número válido para el ID del curso")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
        finally:
            input("\nPresione Enter para volver al menú...")

    def _obtener_profesor(self, id_profesor):
        """Obtiene los detalles completos de un profesor"""
        if not id_profesor:
            return None
            
        try:
            # Necesitaríamos agregar este método en AdminOperations
            profesores = self.operations.listar_profesores()
            return next((p for p in profesores if p['id_profesor'] == id_profesor), None)
        except Exception:
            return None
        
    def _validar_genero(self):
        while True:
            genero = input("Género (M/F): ").upper()
            if genero in ['M', 'F']:
                return genero
            print("❌ Debe ser M o F")
    