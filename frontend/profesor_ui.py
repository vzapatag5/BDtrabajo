from backend.profesor import ProfesorOperations
from tabulate import tabulate

class ProfesorUI:
    def __init__(self, user):
        self.user = user
        self.operations = ProfesorOperations()
        
    def show_menu(self):
        while True:
            print(f"\n=== MENÚ PROFESOR ===")
            print(f"Bienvenido(a) {self.user['nombre']}\n")
            print("1. Gestionar tareas")
            print("2. Gestionar material")
            print("3. Ver mis cursos")
            print("4. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._gestion_tareas()
            elif opcion == "2":
                self._gestion_material()
            elif opcion == "3":
                self._mis_cursos()
            elif opcion == "4":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida")

    def _gestion_tareas(self):
        while True:
            print("\n=== GESTIÓN DE TAREAS ===")
            print("1. Publicar nueva tarea")
            print("2. Ver tareas publicadas")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._publicar_tarea()
            elif opcion == "2":
                self._ver_tareas()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _publicar_tarea(self):
        print("\n=== PUBLICAR NUEVA TAREA ===")
        
        # Mostrar cursos asignados al profesor
        cursos = self.operations.listar_cursos_profesor(self.user['id'])
        if not cursos:
            print("No tienes cursos asignados para publicar tareas")
            return
            
        print("\nTus cursos asignados:")
        print(tabulate(
            [(c['id_curso'], c['nombre']) for c in cursos],
            headers=['ID', 'Nombre del Curso'],
            tablefmt='grid'
        ))
        
        try:
            id_curso = int(input("\nID del curso para la tarea: "))
            if not any(c['id_curso'] == id_curso for c in cursos):
                print("❌ No estás asignado a este curso")
                return
                
            tarea_data = {
                'nombre': input("Nombre de la tarea: "),
                'descripcion': input("Descripción: "),
                'archivo': input("Nombre del archivo: "),
                'fecha_creacion': input("Fecha creación (YYYY-MM-DD): "),
                'fecha_entrega': input("Fecha entrega (YYYY-MM-DD): ")
            }
            
            # Validación básica de fechas
            if len(tarea_data['fecha_creacion']) != 10 or len(tarea_data['fecha_entrega']) != 10:
                print("❌ El formato de fecha debe ser YYYY-MM-DD")
                return
                
            # Llamada corregida - sin id_tarea
            if self.operations.publicar_tarea(id_curso, self.user['id'], **tarea_data):
                print("✅ Tarea publicada correctamente")
            else:
                print("❌ No se pudo publicar la tarea")
                
        except ValueError:
            print("❌ El ID del curso debe ser un número")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")

    def _ver_tareas(self):
        cursos = self.operations.listar_cursos_profesor(self.user['id'])
        
        if not cursos:
            print("No tienes cursos asignados")
            return
            
        print("\nTus cursos:")
        print(tabulate(cursos, headers="keys", tablefmt="pretty"))
        
        id_curso = input("\nID del curso para ver tareas: ")
        tareas = self.operations.listar_tareas_curso(id_curso)
        
        if tareas:
            print("\nTareas publicadas:")
            print(tabulate(tareas, headers="keys", tablefmt="pretty"))
        else:
            print("No hay tareas publicadas en este curso")

    def _gestion_material(self):
        while True:
            print("\n=== GESTIÓN DE MATERIAL ===")
            print("1. Publicar nuevo material")
            print("2. Ver material publicado")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._publicar_material()
            elif opcion == "2":
                print("Función en desarrollo")
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _publicar_material(self):
        print("\n=== NUEVO MATERIAL ===")
        cursos = self.operations.listar_cursos_profesor(self.user['id'])
        
        if not cursos:
            print("No tienes cursos asignados")
            return
            
        print("\nTus cursos:")
        print(tabulate(cursos, headers="keys", tablefmt="pretty"))
        
        id_curso = input("\nID del curso para el material: ")
        
        datos = {
            'id_material': input("ID del material: "),
            'titulo': input("Título: "),
            'descripcion': input("Descripción: "),
            'archivo': input("Nombre del archivo: "),
            'fecha_publicacion': input("Fecha publicación (YYYY-MM-DD): ")
        }
        
        if self.operations.publicar_material(id_curso, self.user['id'], **datos):
            print("✅ Material publicado exitosamente")

    def _mis_cursos(self):
        cursos = self.operations.listar_cursos_profesor(self.user['id'])
        
        if cursos:
            print("\nTus cursos asignados:")
            print(tabulate(cursos, headers="keys", tablefmt="pretty"))
            
            try:
                id_curso = input("\nID del curso para ver estudiantes (Enter para omitir): ")
                if id_curso:
                    id_curso = int(id_curso)  # Convertir a entero
                    # Verificar que el profesor está asignado a este curso
                    if not any(c['id_curso'] == id_curso for c in cursos):
                        print("❌ No estás asignado a este curso")
                        return
                        
                    estudiantes = self.operations.listar_estudiantes_curso(id_curso)
                    if estudiantes:
                        print("\nEstudiantes inscritos:")
                        print(tabulate(estudiantes, headers="keys", tablefmt="pretty"))
                    else:
                        print("No hay estudiantes inscritos")
            except ValueError:
                print("❌ El ID del curso debe ser un número")
        else:
            print("No tienes cursos asignados")