from backend.db import Database

class ProfesorOperations:
    def __init__(self):
        self.db = Database()

    def listar_cursos_profesor(self, id_profesor):
        try:
            query = """
                SELECT c.id_curso, c.nombre, cat.nombre AS categoria
                FROM curso c
                JOIN categoria cat ON c.id_categoria = cat.id_categoria
                WHERE c.id_profesor = %s
            """
            return self.db.execute_query(query, (id_profesor,))
        finally:
            self.db.close()

    def publicar_tarea(self, id_curso, id_profesor, **kwargs):
        db = Database()  # Nueva instancia
        try:
            db.start_transaction()
            query = """
                INSERT INTO asignacion_tarea (
                    id_curso, id_profesor, nombre, 
                    desc_tarea, nombre_archivo, fecha_creacion_tarea, fecha_entrega_tarea
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                id_curso, id_profesor,
                kwargs['nombre'], kwargs['descripcion'],
                kwargs['archivo'], kwargs['fecha_creacion'],
                kwargs['fecha_entrega']
            )
            result = db.execute_query(query, params)
            
            if result:
                db.commit()
                return True
            else:
                db.rollback()
                return False
                
        except Exception as e:
            print(f"Error en publicar_tarea: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def listar_tareas_curso(self, id_curso):
        try:
            return self.db.execute_query("""
                SELECT id_tarea, nombre, desc_tarea, fecha_entrega_tarea
                FROM asignacion_tarea
                WHERE id_curso = %s
            """, (id_curso,))
        finally:
            self.db.close()

    def publicar_material(self, id_curso, **kwargs):
        db = Database()  # Nueva instancia
        try:
            db.start_transaction()
            query = """
                INSERT INTO material (
                    id_curso, titulo, desc_material, 
                    nombre_archivo, fecha_public
                ) VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                id_curso,
                kwargs['titulo'], kwargs['descripcion'],
                kwargs['archivo'], kwargs['fecha_publicacion']
            )
            result = db.execute_query(query, params)
            
            if result:
                db.commit()
                print("✅ Material insertado y transacción confirmada")  # Debug
                return True
            else:
                db.rollback()
                print("❌ Error al insertar material - transacción revertida")  # Debug
                return False
                
        except Exception as e:
            print(f"Error en publicar_material: {e}")
            db.rollback()
            return False
        finally:
            db.close()
            
    def listar_estudiantes_curso(self, id_curso):
        try:
            return self.db.execute_query("""
                SELECT e.id_estudiante, e.nombre, e.email
                FROM estudiante e
                JOIN pago p ON e.id_estudiante = p.id_estudiante
                JOIN matricula m ON p.id_pago = m.id_pago
                WHERE m.id_curso = %s
            """, (id_curso,))
        finally:
            self.db.close()
            
    def crear_foro(self, id_curso, id_profesor, **kwargs):
        db = Database()  # Nueva instancia
        try:
            db.start_transaction()
            query = """
                INSERT INTO creacion_foro (
                    nombre, id_profesor, id_curso, 
                    desc_foro, fecha_creacion_foro, fecha_termin_foro
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                kwargs['nombre'], id_profesor, id_curso,
                kwargs['descripcion'], kwargs['fecha_creacion'],
                kwargs['fecha_termino']
            )
            result = db.execute_query(query, params)
            
            if result:
                db.commit()
                return True
            else:
                db.rollback()
                return False
                
        except Exception as e:
            print(f"Error en crear_foro: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def listar_foros_profesor(self, id_profesor):
        try:
            return self.db.execute_query("""
                SELECT f.id_foro, f.nombre, c.nombre AS nombre_curso, 
                       f.fecha_creacion_foro, f.fecha_termin_foro
                FROM creacion_foro f
                JOIN curso c ON f.id_curso = c.id_curso
                WHERE f.id_profesor = %s
                ORDER BY f.fecha_creacion_foro DESC
            """, (id_profesor,))
        finally:
            self.db.close()

    def listar_foros_disponibles(self, id_profesor):
        try:
            return self.db.execute_query("""
                SELECT f.id_foro, f.nombre, c.nombre AS nombre_curso
                FROM creacion_foro f
                JOIN curso c ON f.id_curso = c.id_curso
                WHERE c.id_profesor = %s OR f.id_profesor = %s
                ORDER BY f.fecha_creacion_foro DESC
            """, (id_profesor, id_profesor))
        finally:
            self.db.close()

    def listar_mensajes_foro(self, id_foro):
        try:
            return self.db.execute_query("""
                SELECT m.id_mensaje, m.nombre, m.desc_msj_foro, m.fecha_envio, 
                       m.id_mensaje_respuesta, p.nombre AS nombre_profesor, 
                       e.nombre AS nombre_estudiante
                FROM mensaje_foro m
                LEFT JOIN profesor p ON m.id_profesor = p.id_profesor
                LEFT JOIN estudiante e ON m.id_estudiante = e.id_estudiante
                WHERE m.id_foro = %s
                ORDER BY m.fecha_envio ASC
            """, (id_foro,))
        finally:
            self.db.close()

    def publicar_mensaje_foro(self, id_foro, id_profesor, **kwargs):
        db = Database()  # Nueva instancia
        try:
            db.start_transaction()
            
            # Primero, obtener el siguiente ID disponible
            max_id_query = "SELECT COALESCE(MAX(id_mensaje), 0) + 1 as next_id FROM mensaje_foro"
            result = db.execute_query(max_id_query)
            next_id = result[0]['next_id'] if result and len(result) > 0 else 1
            
            print(f"Siguiente ID a usar: {next_id}")  # Debug
            
            query = """
                INSERT INTO mensaje_foro (
                    id_mensaje, id_profesor, id_foro, nombre, 
                    desc_msj_foro, fecha_envio, id_mensaje_respuesta
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                next_id,  # Agregar el ID generado
                id_profesor, id_foro,
                kwargs['nombre'], kwargs['descripcion'],
                kwargs['fecha_envio'], kwargs.get('id_mensaje_respuesta')
            )
            
            result = db.execute_query(query, params)
            
            if result:
                db.commit()
                return True
            else:
                db.rollback()
                return False
                
        except Exception as e:
            print(f"Error en publicar_mensaje_foro: {str(e)}")
            db.rollback()
            return False
        finally:
            db.close()
        
    def listar_materiales_profesor(self, id_profesor):
        try:
            # Query corregida - usar directamente la relación con curso
            return self.db.execute_query("""
                SELECT m.id_material, m.titulo, c.nombre AS nombre_curso, 
                    m.fecha_public, m.nombre_archivo, m.desc_material
                FROM material m
                JOIN curso c ON m.id_curso = c.id_curso
                WHERE c.id_profesor = %s
                ORDER BY m.fecha_public DESC
            """, (id_profesor,))
        finally:
            self.db.close()

    def listar_materiales_curso(self, id_curso):
        try:
            return self.db.execute_query("""
                SELECT m.id_material, m.titulo, m.fecha_public, 
                    m.nombre_archivo, m.desc_material, c.nombre AS nombre_curso
                FROM material m
                JOIN curso c ON m.id_curso = c.id_curso
                WHERE m.id_curso = %s
                ORDER BY m.fecha_public DESC
            """, (id_curso,))
        finally:
            self.db.close()