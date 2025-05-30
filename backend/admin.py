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
                    p.nombre AS nombre_profesor,
                    cat.nombre AS nombre_categoria,
                    c.fecha_inicio,
                    c.fecha_fin,
                    c.precio,
                    c.url_contenido,
                    c.periodo,
                    c.año
                FROM curso c
                JOIN profesor p ON c.id_profesor = p.id_profesor
                JOIN categoria cat ON c.id_categoria = cat.id_categoria
                ORDER BY c.id_curso DESC  # Cambiado a ordenar por ID descendente
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
            resultado = self.db.execute_query(query, params)

            if resultado:
                self.db.commit()  # ← AGREGAR ESTA LÍNEA
                return True
            else:
                self.db.rollback()
                return False
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
            # 1. Verificar que el estudiante y curso existen
            estudiante = self.db.execute_query(
                "SELECT 1 FROM estudiante WHERE id_estudiante = %s", 
                (id_estudiante,),
                fetch_one=True
            )
            curso = self.db.execute_query(
                "SELECT 1 FROM curso WHERE id_curso = %s", 
                (id_curso,),
                fetch_one=True
            )
            
            if not estudiante or not curso:
                return False

            # 2. Verificar matrícula existente
            matriculado = self.db.execute_query("""
                SELECT 1 FROM matricula m
                JOIN pago p ON m.id_pago = p.id_pago
                WHERE p.id_estudiante = %s AND m.id_curso = %s
            """, (id_estudiante, id_curso), fetch_one=True)
            
            if matriculado:
                return False

            # 3. Iniciar transacción
            self.db.start_transaction()
            
            # 4. Crear pago y obtener ID
            pago_id = self.db.execute_query(
                """INSERT INTO pago (id_estudiante, valor_pago, comprobante)
                VALUES (%s, 0, 'MATRICULA-ADMIN')""",
                (id_estudiante,),
                return_lastrowid=True
            )
            
            if not pago_id:
                raise Exception("No se pudo crear el pago")
            
            # 5. Crear matrícula
            resultado = self.db.execute_query(
                """INSERT INTO matricula (id_pago, id_curso, fecha_matricula, semestre, año)
                VALUES (%s, %s, CURRENT_DATE, 1, YEAR(CURRENT_DATE))""",
                (pago_id, id_curso)
            )
            
            if not resultado:
                raise Exception("No se pudo crear la matrícula")
            
            # 6. Confirmar transacción
            self.db.commit()
            return True
            
        except Exception as e:
            print(f"Error en BD: {str(e)}")
            self.db.rollback()
            return False
        finally:
            self.db.close()
            
    def obtener_profesor(self, id_profesor):
        try:
            return self.db.execute_query("""
                SELECT id_profesor, nombre, email, genero, 
                       area_principal, area_alternativa
                FROM profesor
                WHERE id_profesor = %s
            """, (id_profesor,))
        finally:
            self.db.close()

    def obtener_ultimo_curso_creado(self):
        try:
            resultados = self.db.execute_query("""
                SELECT c.id_curso, c.nombre AS nombre_curso
                FROM curso c
                ORDER BY c.id_curso DESC
                LIMIT 1
            """)
            return resultados[0] if resultados else None
        except Exception as e:
            print(f"Error al obtener último curso: {str(e)}")
            return None
        finally:
            self.db.close()