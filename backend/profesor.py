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
        try:
            query = """
                INSERT INTO asignacion_tarea (
                    id_tarea, id_curso, id_profesor, nombre, 
                    desc_tarea, nombre_archivo, fecha_creacion_tarea, fecha_entrega_tarea
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                kwargs['id_tarea'], id_curso, id_profesor,
                kwargs['nombre'], kwargs['descripcion'],
                kwargs['archivo'], kwargs['fecha_creacion'],
                kwargs['fecha_entrega']
            )
            return self.db.execute_query(query, params)
        finally:
            self.db.close()

    def listar_tareas_curso(self, id_curso):
        try:
            return self.db.execute_query("""
                SELECT id_tarea, nombre, fecha_entrega_tarea
                FROM asignacion_tarea
                WHERE id_curso = %s
            """, (id_curso,))
        finally:
            self.db.close()

    def publicar_material(self, id_curso, id_profesor, **kwargs):
        try:
            query = """
                INSERT INTO material (
                    id_material, id_curso, id_profesor, 
                    titulo, desc_material, nombre_archivo, fecha_public
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                kwargs['id_material'], id_curso, id_profesor,
                kwargs['titulo'], kwargs['descripcion'],
                kwargs['archivo'], kwargs['fecha_publicacion']
            )
            return self.db.execute_query(query, params)
        finally:
            self.db.close()

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