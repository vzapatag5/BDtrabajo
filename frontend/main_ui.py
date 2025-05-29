from backend.auth import AuthService
from frontend.admin_ui import AdminUI
from frontend.profesor_ui import ProfesorUI
from frontend.estudiante_ui import EstudianteUI

class MainUI:
    def __init__(self):
        self.auth_service = AuthService()
        
    def show_login(self):
        print("\n=== SISTEMA ACADÉMICO ===")
        print("Inicio de Sesión\n")
        
        email = input("Correo electrónico: ")
        password = input("Contraseña: ")
        
        user = self.auth_service.login(email, password)
        
        if user:
            print(f"\n✅ Bienvenido(a) {user['nombre']} ({user['rol'].capitalize()})")
            self._redirect_user(user)
        else:
            print("\n❌ Credenciales incorrectas. Intente nuevamente.")
            
    def _redirect_user(self, user):
        if user['rol'] == 'admin':
            AdminUI(user).show_menu()
        elif user['rol'] == 'profesor':
            ProfesorUI(user).show_menu()
        elif user['rol'] == 'estudiante':
            EstudianteUI(user).show_menu()