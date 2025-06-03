from backend.db import Database

class EstudianteOperations:
    def __init__(self):
        self.db = Database()

    def listar_tareas_estudiante(self, id_estudiante):
        #lista las tareas asignadas al estudiante
        try:
            return self.db.execute_query("""
                SELECT at.nombre FROM asignacion_tarea AS at 
                INNER JOIN entrega_tarea e ON at.id_tarea = e.id_tarea 
                INNER JOIN estudiante AS es ON e.id_estudiante = es.id_estudiante 
                WHERE es.id_estudiante = %s
            """, (id_estudiante,))
        except Exception as e:
            print(f"❌ Error al listar tareas: {e}")
            return []
        finally:
            self.db.close()

    def descargar_material(self, id_material, id_estudiante):
        # Descarga un material específico si el estudiante tiene acceso
        try:
            if not str(id_material).isdigit():
                print("❌ El ID debe ser un número")
                return None

            query = """
                SELECT m.id_material, m.titulo, m.desc_material, 
                    m.nombre_archivo, m.fecha_public
                FROM material m
                JOIN curso c ON m.id_curso = c.id_curso
                JOIN matricula mat ON c.id_curso = mat.id_curso
                JOIN pago p ON mat.id_pago = p.id_pago
                WHERE m.id_material = %s AND p.id_estudiante = %s
            """
            params = (int(id_material), int(id_estudiante))  

            result = self.db.execute_query(query, params)

            if result and len(result) > 0:
                return result[0]
            else:
                print("⚠️ No se encontró material con ese ID o no tienes acceso")
                return None
        except Exception as e:
            print(f"❌ Error al descargar material: {e}")
            return None
        finally:
            self.db.close()
        
    def listar_respuestas_foro(self, id_foro, id_estudiante):
        # Lista las respuestas de un foro específico al que el estudiante tiene acceso
        try:
            return self.db.execute_query("""
                SELECT 
                    mf.id_mensaje, 
                    COALESCE(e.nombre, p.nombre) AS autor,
                    mf.desc_msj_foro AS mensaje,
                    mf.fecha_envio AS fecha
                FROM mensaje_foro mf
                LEFT JOIN estudiante e ON mf.id_estudiante = e.id_estudiante
                LEFT JOIN profesor p ON mf.id_profesor = p.id_profesor
                WHERE mf.id_foro = %s
                AND EXISTS (
                    SELECT 1 
                    FROM creacion_foro cf
                    JOIN curso c ON cf.id_curso = c.id_curso
                    JOIN matricula mat ON c.id_curso = mat.id_curso
                    JOIN pago pa ON mat.id_pago = pa.id_pago
                    WHERE cf.id_foro = mf.id_foro
                        AND pa.id_estudiante = %s
                )
                ORDER BY mf.fecha_envio ASC
            """, (id_foro, id_estudiante)) or []
        except Exception as e:
            print(f"❌ Error al listar respuestas: {e}")
            return []
        finally:
            self.db.close()

    def responder_foro(self, id_foro, id_estudiante, mensaje):
        # Responde a un foro específico si el estudiante tiene acceso
        db_transaccion = None
        try:
            db_transaccion = Database()
            acceso, msg = self._verificar_participacion_foro_interno(db_transaccion, id_foro, id_estudiante)
            if not acceso:
                print(f"❌ {msg}")
                return False
            
            db_transaccion.start_transaction()

            next_id = self._obtener_siguiente_id_mensaje_interno(db_transaccion)
            if not next_id:
                db_transaccion.rollback()
                return False

            estudiante_info = db_transaccion.execute_query(
                "SELECT nombre FROM estudiante WHERE id_estudiante = %s", 
                (id_estudiante,)
            )
            nombre_autor = estudiante_info[0]['nombre'] if estudiante_info else f"Estudiante {id_estudiante}"

            resultado = db_transaccion.execute_query("""
                INSERT INTO mensaje_foro (
                    id_mensaje, id_estudiante, id_foro, 
                    nombre, desc_msj_foro, fecha_envio
                ) VALUES (%s, %s, %s, %s, %s, NOW())
            """, (next_id, id_estudiante, id_foro, nombre_autor, mensaje))

            if resultado:
                db_transaccion.commit()
                print("✅ Transacción confirmada")
                return True
            else:
                db_transaccion.rollback()
                return False

        except Exception as e:
            print(f"❌ Error al responder: {str(e)}")
            if db_transaccion:
                db_transaccion.rollback()
            return False
        finally:
            if db_transaccion:
                db_transaccion.close()

    def _obtener_siguiente_id_mensaje(self):
        # Obtiene el siguiente ID disponible para un nuevo mensaje en el foro
        try:
            result = self.db.execute_query("""
                SELECT IFNULL(MAX(id_mensaje), 0) + 1 AS next_id 
                FROM mensaje_foro
            """)
            
            if result and len(result) > 0:
                return result[0]['next_id']
            else:
                return 1
                
        except Exception as e:
            print(f"❌ Error al obtener siguiente ID: {e}")
            return None
        finally:
            self.db.close()

    def _obtener_siguiente_id_mensaje_interno(self, db_connection):
        # Obtiene el siguiente ID disponible para un nuevo mensaje en el foro dentro de una transacción
        try:
            result = db_connection.execute_query("""
                SELECT IFNULL(MAX(id_mensaje), 0) + 1 AS next_id 
                FROM mensaje_foro
            """)
            
            if result and len(result) > 0:
                return result[0]['next_id']
            else:
                return 1
                
        except Exception as e:
            print(f"❌ Error al obtener siguiente ID: {e}")
            return None

    def _verificar_participacion_foro_interno(self, db_connection, id_foro, id_estudiante):
        # Verifica si el estudiante tiene acceso a un foro específico dentro de una transacción
        try:
            resultado = db_connection.execute_query("""
                SELECT cf.id_foro
                FROM creacion_foro cf
                JOIN curso c ON cf.id_curso = c.id_curso
                JOIN matricula mat ON c.id_curso = mat.id_curso
                JOIN pago p ON mat.id_pago = p.id_pago
                WHERE cf.id_foro = %s
                AND p.id_estudiante = %s
                AND cf.fecha_termin_foro >= CURDATE()
                LIMIT 1
            """, (id_foro, id_estudiante))
            
            return bool(resultado), "Foro disponible" if resultado else "No tienes acceso a este foro"
        except Exception as e:
            return False, f"Error de verificación: {str(e)}"
            
    def listar_materiales(self):
        # Lista todos los materiales disponibles en la base de datos
        try:
            return self.db.execute_query("""
                SELECT id_material, titulo 
                FROM material 
                ORDER BY id_material
            """) or []
        except Exception as e:
            print(f"Error al listar materiales: {e}")
            return []
        finally:
            self.db.close()

    def listar_materiales_estudiante(self, id_estudiante):
        # Lista los materiales a los que un estudiante tiene acceso
        try:
            return self.db.execute_query("""
                SELECT m.id_material, m.titulo 
                FROM material m
                JOIN curso c ON m.id_curso = c.id_curso
                JOIN matricula mat ON c.id_curso = mat.id_curso
                JOIN pago p ON mat.id_pago = p.id_pago
                WHERE p.id_estudiante = %s
                ORDER BY m.id_material
            """, (id_estudiante,)) or []
        except Exception as e:
            print(f"Error al listar materiales del estudiante: {e}")
            return []
        finally:
            self.db.close()
        
    def listar_foros_disponibles(self, id_estudiante):
        # Lista los foros activos a los que un estudiante tiene acceso
        try:
            table_exists = self.db.execute_query("""
                SELECT COUNT(*) AS existe 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = 'creacion_foro'
            """)
            
            if not table_exists or table_exists[0]['existe'] == 0:
                print("⚠️ La tabla de foros (creacion_foro) no existe en la base de datos")
                return []
                
            # Obtener foros activos a los que pertenece el estudiante
            foros = self.db.execute_query("""
                SELECT cf.id_foro, cf.nombre, cf.desc_foro AS descripcion, 
                    cf.fecha_creacion_foro, cf.fecha_termin_foro
                FROM creacion_foro cf
                JOIN foro_usuario fu ON cf.id_foro = fu.id_foro
                WHERE cf.fecha_termin_foro >= CURDATE()
                AND fu.id_estudiante = %s
                ORDER BY cf.fecha_creacion_foro DESC
            """, (id_estudiante,))
            
            return foros if foros else []
            
        except Exception as e:
            print(f"❌ Error al verificar foros: {e}")
            return []
        finally:
            self.db.close()

    def verificar_participacion_foro(self, id_foro, id_estudiante):
        # Verifica si el estudiante tiene acceso a un foro específico
        try:
            resultado = self.db.execute_query("""
                SELECT cf.id_foro
                FROM creacion_foro cf
                JOIN curso c ON cf.id_curso = c.id_curso
                JOIN matricula mat ON c.id_curso = mat.id_curso
                JOIN pago p ON mat.id_pago = p.id_pago
                WHERE cf.id_foro = %s
                AND p.id_estudiante = %s
                AND cf.fecha_termin_foro >= CURDATE()
                LIMIT 1
            """, (id_foro, id_estudiante))
            
            return bool(resultado), "Foro disponible" if resultado else "No tienes acceso a este foro"
        except Exception as e:
            return False, f"Error de verificación: {str(e)}"
        finally:
            self.db.close()