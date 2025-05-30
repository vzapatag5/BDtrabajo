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
                port=3307,
                password="Fito123",
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

    def execute_query(self, query, args=None, fetch_one=False, return_lastrowid=False):
        """Ejecuta una consulta SQL con manejo robusto de errores"""
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
                
                # No hacemos commit automático para manejar transacciones explícitas
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
        """Inicia una transacción explícita"""
        if self.is_connected():
            self.connection.begin()

    def commit(self):
        """Confirma una transacción"""
        if self.is_connected():
            self.connection.commit()

    def rollback(self):
        """Revierte una transacción"""
        if self.is_connected():
            self.connection.rollback()

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