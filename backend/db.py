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
                port=3307, #cambiar según la conexión
                password="Fito123", #cambiar según la conexión
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
        try:
            if self.connection and self.connection.open:
                self.connection.ping(reconnect=True)
                return True
            return False
        except:
            return False

    def execute_query(self, query, args=None, fetch_one=False, return_lastrowid=False):
        try:
            if not self.is_connected():
                print("⚠️ Reconectando a la base de datos...")
                if not self._connect():
                    return None

            with self.connection.cursor() as cursor:
                cursor.execute(query, args or ())
                
                if return_lastrowid:
                    result = cursor.lastrowid
                elif query.strip().upper().startswith('SELECT'):
                    result = cursor.fetchone() if fetch_one else cursor.fetchall()
                else:
                    result = cursor.rowcount > 0
                return result
                
        except OperationalError as e:
            print(f"❌ Error de conexión: {e}")
            self.connection = None
            return None
        except Exception as e:
            print(f"❌ Error en consulta: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def start_transaction(self):
        if self.is_connected():
            self.connection.begin()

    def commit(self):
        if self.is_connected():
            self.connection.commit()

    def rollback(self):
        if self.is_connected():
            self.connection.rollback()

    def close(self):
        try:
            if self.connection and self.connection.open:
                self.connection.close()
                print("🔌 Conexión a BD cerrada")
        except Exception as e:
            print(f"⚠️ Error al cerrar conexión: {e}")
        finally:
            self.connection = None