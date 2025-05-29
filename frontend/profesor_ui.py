from backend.profesor import ProfesorOperations
from tabulate import tabulate

from backend.profesor import ProfesorOperations
from tabulate import tabulate
from datetime import datetime

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
            print("3. Gestionar foros")
            print("4. Ver mis cursos")
            print("5. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._gestion_tareas()
            elif opcion == "2":
                self._gestion_material()
            elif opcion == "3":
                self._gestion_foros()
            elif opcion == "4":
                self._mis_cursos()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida")

    # ... (mantén los métodos existentes como _gestion_tareas, _publicar_tarea, etc.)

    def _gestion_foros(self):
        while True:
            print("\n=== GESTIÓN DE FOROS ===")
            print("1. Crear nuevo foro")
            print("2. Ver mis foros")
            print("3. Participar en foro")
            print("4. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._crear_foro()
            elif opcion == "2":
                self._ver_mis_foros()
            elif opcion == "3":
                self._participar_en_foro()
            elif opcion == "4":
                break
            else:
                print("Opción no válida")

    def _crear_foro(self):
        print("\n=== CREAR NUEVO FORO ===")
        
        cursos = self.operations.listar_cursos_profesor(self.user['id'])
        if not cursos:
            print("No tienes cursos asignados para crear foros")
            return
            
        print("\nTus cursos asignados:")
        print(tabulate(
            [(c['id_curso'], c['nombre']) for c in cursos],
            headers=['ID', 'Nombre del Curso'],
            tablefmt='grid'
        ))
        
        try:
            id_curso = int(input("\nID del curso para el foro: "))
            if not any(c['id_curso'] == id_curso for c in cursos):
                print("❌ No estás asignado a este curso")
                return
                
            foro_data = {
                'nombre': input("Nombre del foro: "),
                'descripcion': input("Descripción: "),
                'fecha_creacion': datetime.now().strftime('%Y-%m-%d'),
                'fecha_termino': input("Fecha de cierre (YYYY-MM-DD): ")
            }
            
            if len(foro_data['fecha_termino']) != 10:
                print("❌ El formato de fecha debe ser YYYY-MM-DD")
                return
                
            if self.operations.crear_foro(id_curso, self.user['id'], **foro_data):
                print("✅ Foro creado correctamente")
            else:
                print("❌ No se pudo crear el foro")
                
        except ValueError:
            print("❌ El ID del curso debe ser un número")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")

    def _ver_mis_foros(self):
        print("\n=== MIS FOROS ===")
        foros = self.operations.listar_foros_profesor(self.user['id'])
        
        if foros:
            print("\nForos creados por ti:")
            print(tabulate(
                [(f['id_foro'], f['nombre'], f['nombre_curso'], f['fecha_creacion_foro'], f['fecha_termin_foro']) 
                 for f in foros],
                headers=['ID', 'Nombre Foro', 'Curso', 'Fecha Creación', 'Fecha Cierre'],
                tablefmt='grid'
            ))
        else:
            print("No has creado ningún foro")

    def _participar_en_foro(self):
        print("\n=== PARTICIPAR EN FORO ===")
        
        # Mostrar foros de los cursos del profesor
        foros = self.operations.listar_foros_disponibles(self.user['id'])
        
        if not foros:
            print("No hay foros disponibles en tus cursos")
            return
            
        print("\nForos disponibles:")
        print(tabulate(
            [(f['id_foro'], f['nombre'], f['nombre_curso']) for f in foros],
            headers=['ID', 'Nombre Foro', 'Curso'],
            tablefmt='grid'
        ))
        
        try:
            id_foro = int(input("\nID del foro para participar: "))
            if not any(f['id_foro'] == id_foro for f in foros):
                print("❌ No tienes acceso a este foro")
                return
                
            print("\n1. Ver mensajes existentes")
            print("2. Publicar nuevo mensaje")
            print("3. Responder a mensaje existente")
            opcion = input("\nSeleccione una acción: ")
            
            if opcion == "1":
                self._ver_mensajes_foro(id_foro)
            elif opcion == "2":
                self._publicar_mensaje_foro(id_foro, None)  # None indica que no es respuesta
            elif opcion == "3":
                # Primero mostrar los mensajes disponibles
                self._ver_mensajes_foro(id_foro)
                
                # Validar que haya mensajes a los que responder
                mensajes = self.operations.listar_mensajes_foro(id_foro)
                if not mensajes:
                    print("No hay mensajes a los que responder en este foro")
                    return
                    
                try:
                    id_respuesta = int(input("\nID del mensaje al que responder (0 para cancelar): "))
                    if id_respuesta == 0:
                        return
                        
                    # Verificar que el mensaje al que se responde existe
                    if not any(m['id_mensaje'] == id_respuesta for m in mensajes):
                        print("❌ El ID del mensaje no existe en este foro")
                        return
                        
                    self._publicar_mensaje_foro(id_foro, id_respuesta)
                except ValueError:
                    print("❌ Debes ingresar un número válido")
            else:
                print("Opción no válida")
                
        except ValueError:
            print("❌ El ID debe ser un número")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
    def _ver_mensajes_foro(self, id_foro):
        mensajes = self.operations.listar_mensajes_foro(id_foro)
        
        if mensajes:
            print("\nMensajes en el foro:")
            for msg in mensajes:
                autor = f"Prof. {msg['nombre_profesor']}" if msg['nombre_profesor'] else f"Est. {msg['nombre_estudiante']}"
                respuesta = f" (Respuesta a #{msg['id_mensaje_respuesta']})" if msg['id_mensaje_respuesta'] else ""
                print(f"\n[{msg['id_mensaje']}] {autor}{respuesta} - {msg['fecha_envio']}")
                print(f"Título: {msg['nombre']}")
                print(f"Mensaje: {msg['desc_msj_foro']}")
        else:
            print("No hay mensajes en este foro")

    def _publicar_mensaje_foro(self, id_foro, id_respuesta=None):
        print("\n=== NUEVO MENSAJE ===")
        
        mensaje_data = {
            'nombre': input("Título del mensaje: "),
            'descripcion': input("Contenido del mensaje: "),
            'fecha_envio': datetime.now().strftime('%Y-%m-%d'),
            'id_mensaje_respuesta': id_respuesta if id_respuesta else None  # Asegurar None si es 0
        }
        
        # Debug: Mostrar datos que se enviarán
        print(f"\nDatos a enviar: {mensaje_data}")
        
        if self.operations.publicar_mensaje_foro(id_foro, self.user['id'], **mensaje_data):
            print("✅ Mensaje publicado correctamente")
        else:
            print("❌ No se pudo publicar el mensaje")

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
                self._ver_mis_materiales()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _publicar_material(self):
        print("\n=== PUBLICAR NUEVO MATERIAL ===")
        cursos = self.operations.listar_cursos_profesor(self.user['id'])
        
        if not cursos:
            print("No tienes cursos asignados")
            return
            
        print("\nTus cursos:")
        print(tabulate(
            [(c['id_curso'], c['nombre']) for c in cursos],
            headers=['ID', 'Nombre del Curso'],
            tablefmt='grid'
        ))
        
        try:
            id_curso = int(input("\nID del curso para el material: "))
            if not any(c['id_curso'] == id_curso for c in cursos):
                print("❌ No estás asignado a este curso")
                return
            
            material_data = {
                'titulo': input("Título del material: "),
                'descripcion': input("Descripción: "),
                'archivo': input("Nombre del archivo (ej: guia.pdf): "),
                'fecha_publicacion': datetime.now().strftime('%Y-%m-%d')
            }
            
            if self.operations.publicar_material(id_curso, **material_data):
                print("✅ Material publicado exitosamente")
            else:
                print("❌ Error al publicar el material")
                
        except ValueError:
            print("❌ El ID del curso debe ser un número")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            
    def _ver_mis_materiales(self):
        print("\n=== MIS MATERIALES PUBLICADOS ===")
        materiales = self.operations.listar_materiales_profesor(self.user['id'])
        
        if materiales:
            print(tabulate(
                [(m['id_material'], m['titulo'], m['nombre_curso'], 
                m['fecha_public'], m['nombre_archivo'], m['desc_material']) 
                for m in materiales],
                headers=['ID', 'Título', 'Curso', 'Fecha', 'Archivo', 'Descripción'],
                tablefmt='grid'
            ))
        else:
            print("No has publicado ningún material")

        def _ver_materiales_curso(self):
            cursos = self.operations.listar_cursos_profesor(self.user['id'])
            
            if not cursos:
                print("No tienes cursos asignados")
                return
                
            print("\nTus cursos:")
            print(tabulate(
                [(c['id_curso'], c['nombre']) for c in cursos],
                headers=['ID', 'Nombre del Curso'],
                tablefmt='grid'
            ))
            
            try:
                id_curso = int(input("\nID del curso para ver materiales: "))
                if not any(c['id_curso'] == id_curso for c in cursos):
                    print("❌ No estás asignado a este curso")
                    return
                    
                materiales = self.operations.listar_materiales_curso(id_curso)
                
                if materiales:
                    print("\nMateriales del curso:")
                    print(tabulate(
                        [(m['id_material'], m['titulo'], m['fecha_public'], 
                        m['nombre_archivo'], m['desc_material']) 
                        for m in materiales],
                        headers=['ID', 'Título', 'Fecha', 'Archivo', 'Descripción'],
                        tablefmt='grid'
                    ))
                else:
                    print("Este curso no tiene materiales publicados")
                    
            except ValueError:
                print("❌ El ID del curso debe ser un número")

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