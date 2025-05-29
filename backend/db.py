import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import OperationalError

class Database:
    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = pymysql.connect(
                host="localhost",
                user="root",
                port=3306,
                password="",
                database="sistema_nodo",
                cursorclass=DictCursor,
                autocommit=False
            )
            print("✅ Conexión a BD establecida")
            return True
        except OperationalError as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def is_connected(self):
        """Verifica si la conexión está activa"""
        try:
            if self.connection and self.connection.open:
                self.connection.ping(reconnect=True)
                return True
            return False
        except:
            return False

    def execute_query(self, query, args=None):
        """Ejecuta una consulta SQL con manejo robusto de errores"""
        try:
            # Verificar y reconectar si es necesario
            if not self.is_connected():
                print("⚠️ Reconectando a la base de datos...")
                if not self._connect():
                    return None

            with self.connection.cursor() as cursor:
                cursor.execute(query, args or ())
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                self.connection.commit()
                return True
        except OperationalError as e:
            print(f"❌ Error de conexión: {e}")
            self.connection = None
            return None
        except Exception as e:
            print(f"❌ Error en consulta: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def close(self):
        """Cierra la conexión de manera segura"""
        try:
            if self.connection and self.connection.open:
                self.connection.close()
                print("🔌 Conexión a BD cerrada")
        except Exception as e:
            print(f"⚠️ Error al cerrar conexión: {e}")
        finally:
            self.connection = None