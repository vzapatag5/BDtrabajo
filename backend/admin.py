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

    def listar_cursos(self):
        try:
            return self.db.execute_query("""
                SELECT 
                    c.id_curso, 
                    c.nombre AS nombre_curso,
                    p.nombre AS nombre_profesor,  # Alias explícito
                    cat.nombre AS nombre_categoria,
                    c.fecha_inicio,
                    c.fecha_fin,
                    c.precio
                FROM curso c
                JOIN profesor p ON c.id_profesor = p.id_profesor
                JOIN categoria cat ON c.id_categoria = cat.id_categoria
                ORDER BY c.fecha_inicio DESC
            """)
        except Exception as e:
            print(f"Error en la consulta: {str(e)}")
            return []
        finally:
            self.db.close()

    def listar_estudiantes_no_matriculados(self, id_curso):
        try:
            return self.db.execute_query("""
                SELECT 
                    e.id_estudiante, 
                    e.nombre AS nombre_estudiante,  # Alias consistente
                    e.email
                FROM estudiante e
                WHERE e.id_estudiante NOT IN (
                    SELECT p.id_estudiante
                    FROM pago p
                    JOIN matricula m ON p.id_pago = m.id_pago
                    WHERE m.id_curso = %s
                )
                ORDER BY e.nombre
            """, (id_curso,))
        finally:
            self.db.close()
        
    def listar_profesores(self):
        try:
            return self.db.execute_query("""
                SELECT id_profesor, nombre, area_principal, email
                FROM profesor
                ORDER BY nombre
            """)
        finally:
            self.db.close()

    def listar_categorias(self):
        try:
            return self.db.execute_query("""
                SELECT id_categoria, nombre
                FROM categoria
                ORDER BY nombre
            """)
        finally:
            self.db.close()


    def insertar_curso(self, **kwargs):
        try:
            query = """
                INSERT INTO curso (
                    id_profesor, nombre, id_categoria, 
                    url_contenido, periodo, precio, año, 
                    fecha_inicio, fecha_fin
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                kwargs['id_profesor'], kwargs['nombre'],
                kwargs['id_categoria'], kwargs['url_contenido'],
                kwargs['periodo'], kwargs['precio'], kwargs['año'],
                kwargs['fecha_inicio'], kwargs['fecha_fin']
            )
            return self.db.execute_query(query, params)
        finally:
            self.db.close()
            
    def listar_cursos_completos(self):
        try:
            return self.db.execute_query("""
                SELECT c.id_curso, c.nombre, 
                    p.nombre AS profesor, 
                    cat.nombre AS categoria
                FROM curso c
                JOIN profesor p ON c.id_profesor = p.id_profesor
                JOIN categoria cat ON c.id_categoria = cat.id_categoria
                ORDER BY c.nombre
            """)
        finally:
            self.db.close()
            
    def asignar_estudiante_curso(self, id_estudiante, id_curso):
        try:
            # 1. Verificar matrícula existente
            matriculado = self.db.execute_query("""
                SELECT 1 FROM matricula m
                JOIN pago p ON m.id_pago = p.id_pago
                WHERE p.id_estudiante = %s AND m.id_curso = %s
            """, (id_estudiante, id_curso))
            
            if matriculado:
                return False

            # 2. Crear pago y matrícula en una sola transacción
            return self.db.execute_query("""
                BEGIN;
                INSERT INTO pago (id_estudiante, valor_pago, comprobante)
                VALUES (%s, 0, 'MATRICULA-ADMIN');
                
                INSERT INTO matricula (id_pago, id_curso, fecha_matricula, semestre, año)
                VALUES (LAST_INSERT_ID(), %s, CURRENT_DATE, 1, YEAR(CURRENT_DATE));
                COMMIT;
            """, (id_estudiante, id_curso))
            
        except Exception as e:
            print(f"Error en BD: {str(e)}")
            self.db.execute_query("ROLLBACK;")
            return False
        finally:
            self.db.close()