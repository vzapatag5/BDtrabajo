from backend.db import Database

class AdminOperations:
    def __init__(self):
        self.db = Database()
    
    # Estudiantes
    def listar_estudiantes(self):
        try:
            return self.db.execute_query("SELECT id_estudiante, id_nodo, nombre, email, genero FROM estudiante")
        finally:
            self.db.close()
    
    def insertar_estudiante(self, **kwargs):
        try:
            query = """
                INSERT INTO estudiante (id_estudiante, id_nodo, nombre, email, genero, contrasena)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                kwargs['id_estudiante'], kwargs['id_nodo'], kwargs['nombre'],
                kwargs['email'], kwargs['genero'], kwargs['contrasena']
            )
            return self.db.execute_query(query, params)
        finally:
            self.db.close()

    # Profesores
    def listar_profesores(self):
        try:
            return self.db.execute_query("SELECT id_profesor, nombre, email, genero FROM profesor")
        finally:
            self.db.close()
    
    def insertar_profesor(self, **kwargs):
        try:
            query = """
                INSERT INTO profesor (id_profesor, nombre, email, genero, 
                area_principal, area_alternativa, contrasena)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                kwargs['id_profesor'], kwargs['nombre'], kwargs['email'],
                kwargs['genero'], kwargs['area_principal'], 
                kwargs.get('area_alternativa', ''), kwargs['contrasena']
            )
            return self.db.execute_query(query, params)
        finally:
            self.db.close()

    # Cursos
    def listar_cursos(self):
        try:
            return self.db.execute_query("""
                SELECT c.id_curso, c.nombre, p.nombre AS profesor, cat.nombre AS categoria
                FROM curso c
                JOIN profesor p ON c.id_profesor = p.id_profesor
                JOIN categoria cat ON c.id_categoria = cat.id_categoria
            """)
        finally:
            self.db.close()
    
    def insertar_curso(self, **kwargs):
        try:
            query = """
                INSERT INTO curso (id_curso, id_profesor, nombre, id_categoria, 
                url_contenido, periodo, precio, año, fecha_inicio, fecha_fin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                kwargs['id_curso'], kwargs['id_profesor'], kwargs['nombre'],
                kwargs['id_categoria'], kwargs['url_contenido'], kwargs['periodo'],
                kwargs['precio'], kwargs['año'], kwargs['fecha_inicio'], kwargs['fecha_fin']
            )
            return self.db.execute_query(query, params)
        finally:
            self.db.close()

    # Reportes
    def listar_todos_usuarios(self):
        try:
            return self.db.execute_query("""
                SELECT id_admin as id, nombre, email, 'admin' as rol FROM adminis
                UNION ALL
                SELECT id_profesor as id, nombre, email, 'profesor' as rol FROM profesor
                UNION ALL
                SELECT id_estudiante as id, nombre, email, 'estudiante' as rol FROM estudiante
            """)
        finally:
            self.db.close()