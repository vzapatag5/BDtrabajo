from backend.db import Database

class AuthService:
    def __init__(self):
        self.db = Database()
        
    def login(self, email, password):
        try:
            # Admin
            admin = self._authenticate("adminis", "id_admin", email, password, "admin")
            if admin: return admin
            
            # Profesor
            profesor = self._authenticate("profesor", "id_profesor", email, password, "profesor")
            if profesor: return profesor
            
            # Estudiante
            estudiante = self._authenticate("estudiante", "id_estudiante", email, password, "estudiante")
            if estudiante:
                estudiante["id_estudiante"] = estudiante["id"] 
                return estudiante
                
            print("⚠️ Usuario no encontrado o credenciales incorrectas")
            return None
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            return None
        finally:
            self.db.close()

    def _authenticate(self, table, id_field, email, password, rol):
        query = f"SELECT {id_field} as id, nombre, email, genero FROM {table} WHERE email=%s AND contrasena=%s"
        result = self.db.execute_query(query, (email, password))
        if result and len(result) > 0:
            result[0]["rol"] = rol
            return result[0]
        return None