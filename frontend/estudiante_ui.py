from backend.estudiante import EstudianteOperations
from tabulate import tabulate

class EstudianteUI:
    def __init__(self, user):
        self.user = user
        self.operations = EstudianteOperations()
        
    def show_menu(self):
        while True:
            print(f"\n=== MENÚ ESTUDIANTE ===")
            print(f"Bienvenido(a) {self.user['nombre']}\n")
            print("1. Ver tareas")
            print("2. Descargar material")
            print("3. Participar en foros")
            print("4. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._ver_tareas()
            elif opcion == "2":
                self._descargar_material()
            elif opcion == "3":
                self._foros()
            elif opcion == "4":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida")

    def _ver_tareas(self):
        tareas = self.operations.listar_tareas_estudiante(self.user['id_estudiante'])
        
        if tareas:
            print("\nTus tareas asignadas:")
            print(tabulate(tareas, headers="keys", tablefmt="pretty"))
        else:
            print("No tienes tareas asignadas")

    def _descargar_material(self):
        print("\n=== DESCARGAR MATERIAL ===")
        print("Materiales disponibles para tus cursos:")
        
        try:
            materiales = self.operations.listar_materiales_estudiante(self.user['id_estudiante'])
            if materiales:
                print(tabulate(
                    [(m['id_material'], m['titulo']) for m in materiales],
                    headers=['ID', 'Título'],
                    tablefmt='pretty'
                ))
            else:
                print("No hay materiales disponibles para tus cursos")
                return
        except Exception as e:
            print(f"❌ Error al listar materiales: {e}")
            return

        try:
            id_material = input("\nIngrese el ID del material a descargar: ")
            # Pasa el id_estudiante como segundo argumento
            material = self.operations.descargar_material(id_material, self.user['id_estudiante'])
            
            if material:
                print("\n📄 DETALLES DEL MATERIAL")
                print(f"ID: {material['id_material']}")
                print(f"Título: {material['titulo']}")
                print(f"Descripción: {material['desc_material']}")
                print(f"Archivo: {material['nombre_archivo']}")
                print(f"Fecha: {material['fecha_public']}")
                print("\n✅ Puede descargarlo desde la plataforma")
            else:
                print("❌ Material no encontrado o no pertenece a tus cursos")
        except Exception as e:
            print(f"❌ Error al descargar material: {e}")

    def _foros(self):
        while True:
            print("\n=== FOROS ===")
            print("1. Ver respuestas en foro")
            print("2. Responder en foro")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._ver_respuestas_foro()
            elif opcion == "2":
                self._responder_foro()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _ver_respuestas_foro(self):
        """Muestra respuestas de foros accesibles"""
        try:
            # Listar foros disponibles primero
            foros = self.operations.listar_foros_disponibles(self.user['id_estudiante'])
            if not foros:
                print("\n⚠️ No tienes acceso a ningún foro activo")
                return

            print("\nForos disponibles:")
            print(tabulate(
                [(f['id_foro'], f['nombre']) for f in foros],
                headers=['ID', 'Nombre'],
                tablefmt='pretty'
            ))

            id_foro = input("\nIngrese ID del foro: ")
            respuestas = self.operations.listar_respuestas_foro(id_foro, self.user['id_estudiante'])
            
            if respuestas:
                print("\n💬 Respuestas:")
                print(tabulate(respuestas, headers="keys", tablefmt="pretty"))
            else:
                print("\nNo hay respuestas o no tienes acceso")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _responder_foro(self):
        """Interfaz mejorada para responder en foros"""
        print("\n=== RESPONDER EN FORO ===")
        
        try:
            # Listar foros disponibles
            foros = self.operations.listar_foros_disponibles(self.user['id_estudiante'])
            if not foros:
                print("\n⚠️ No hay foros disponibles activos")
                print("Puede que todos los foros hayan expirado o no existan foros creados")
                return
                
            print("\nForos activos disponibles:")
            tabla_foros = []
            for foro in foros:
                tabla_foros.append([
                    foro['id_foro'], 
                    foro['nombre'], 
                    foro.get('descripcion', 'Sin descripción')[:50] + ('...' if len(str(foro.get('descripcion', ''))) > 50 else ''),
                    foro.get('fecha_termin_foro', 'No especificada')
                ])
            
            print(tabulate(
                tabla_foros,
                headers=['ID', 'Nombre', 'Descripción', 'Fecha Límite'],
                tablefmt='grid'
            ))
            
            # Solicitar ID del foro
            id_foro_input = input("\nIngrese ID del foro: ").strip()
            if not id_foro_input.isdigit():
                print("❌ El ID debe ser un número")
                return
                
            id_foro = int(id_foro_input)
            
            # Verificar que el foro seleccionado existe en la lista
            foro_valido = any(f['id_foro'] == id_foro for f in foros)
            if not foro_valido:
                print("❌ El ID del foro no está en la lista de foros disponibles")
                return
            
            # Verificar participación en el foro
            puede_participar, mensaje_estado = self.operations.verificar_participacion_foro(
                id_foro, self.user['id_estudiante']
            )
            
            if not puede_participar:
                print(f"❌ {mensaje_estado}")
                return
            
            print(f"✅ {mensaje_estado}")
            
            # Solicitar mensaje
            print("\nEscribe tu respuesta (presiona Enter dos veces para enviar):")
            mensaje_lines = []
            empty_line_count = 0
            
            while empty_line_count < 2:
                line = input()
                if line.strip() == "":
                    empty_line_count += 1
                else:
                    empty_line_count = 0
                mensaje_lines.append(line)
            
            # Unir las líneas y limpiar
            mensaje = '\n'.join(mensaje_lines[:-2]).strip()  # Remover las dos líneas vacías finales
            
            if not mensaje:
                print("❌ La respuesta no puede estar vacía")
                return

            # Confirmar envío
            print(f"\n📝 Vista previa de tu mensaje:")
            print("-" * 50)
            print(mensaje)
            print("-" * 50)
            
            confirmacion = input("\n¿Confirmas el envío? (s/n): ").lower().strip()
            if confirmacion not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Envío cancelado")
                return

            # Enviar respuesta
            if self.operations.responder_foro(id_foro, self.user['id_estudiante'], mensaje):
                print("\n🎉 ¡Respuesta publicada exitosamente!")
                
                # Preguntar si quiere ver las respuestas del foro
                ver_respuestas = input("\n¿Deseas ver todas las respuestas del foro? (s/n): ").lower().strip()
                if ver_respuestas in ['s', 'si', 'sí', 'y', 'yes']:
                    print(f"\n=== RESPUESTAS DEL FORO ===")
                    respuestas = self.operations.listar_respuestas_foro(id_foro)
                    if respuestas:
                        print(tabulate(respuestas, headers="keys", tablefmt="pretty"))
                    else:
                        print("No se pudieron cargar las respuestas")
            else:
                print("\n❌ No se pudo publicar la respuesta. Inténtalo de nuevo.")
                
        except KeyboardInterrupt:
            print("\n\n❌ Operación cancelada por el usuario")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("Por favor, contacta al administrador del sistema")