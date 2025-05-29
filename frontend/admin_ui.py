from backend.admin import AdminOperations
from tabulate import tabulate

class AdminUI:
    def __init__(self, user):
        self.user = user
        self.operations = AdminOperations() 
        
    def show_menu(self):
        while True:
            print("\n=== MENÚ ADMINISTRADOR ===")
            print("1. Gestión de Estudiantes")
            print("2. Gestión de Profesores")
            print("3. Gestión de Cursos")
            print("4. Reportes")
            print("5. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self._gestion_estudiantes()
            elif opcion == "2":
                self._gestion_profesores()
            elif opcion == "3":
                self._gestion_cursos()
            elif opcion == "4":
                self._reportes()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida")

    def _gestion_estudiantes(self):
           while True:
            print("\n=== GESTIÓN DE ESTUDIANTES ===")
            print("1. Listar estudiantes")
            print("2. Agregar estudiante")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                estudiantes = self.operations.listar_estudiantes()
                if estudiantes:
                    print(tabulate(estudiantes, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay estudiantes registrados")
            elif opcion == "2":
                self._agregar_estudiante()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")
                
    def _listar_estudiantes(self):
        try:
            return self.db.execute_query("SELECT id_estudiante, id_nodo, nombre, email, genero FROM estudiante")
        finally:
            self.db.close()

    def _agregar_estudiante(self):
        print("\n=== NUEVO ESTUDIANTE ===")
        datos = {
            'id_estudiante': input("ID: "),
            'id_nodo': input("ID de nodo: "),
            'nombre': input("Nombre completo: "),
            'email': input("Email: "),
            'genero': self._validar_genero(),
            'contrasena': input("Contraseña: ")
        }
        
        if self.operations.insertar_estudiante(**datos):
            print("✅ Estudiante registrado exitosamente")

    def _gestion_profesores(self):
        while True:
            print("\n=== GESTIÓN DE PROFESORES ===")
            print("1. Listar profesores")
            print("2. Agregar profesor")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                profesores = self.operations.listar_profesores()
                if profesores:
                    print(tabulate(profesores, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay profesores registrados")
            elif opcion == "2":
                self._agregar_profesor()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _agregar_profesor(self):
        print("\n=== NUEVO PROFESOR ===")
        datos = {
            'id_profesor': input("ID: "),
            'nombre': input("Nombre completo: "),
            'email': input("Email: "),
            'genero': self._validar_genero(),
            'area_principal': input("Área principal: "),
            'area_alternativa': input("Área alternativa (opcional): "),
            'contrasena': input("Contraseña: ")
        }
        
        if self.operations.insertar_profesor(**datos):
            print("✅ Profesor registrado exitosamente")

    def _gestion_cursos(self):
        while True:
            print("\n=== GESTIÓN DE CURSOS ===")
            print("1. Listar cursos")
            print("2. Agregar curso")
            print("3. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                cursos = self.operations.listar_cursos()
                if cursos:
                    print(tabulate(cursos, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay cursos registrados")
            elif opcion == "2":
                self._agregar_curso()
            elif opcion == "3":
                break
            else:
                print("Opción no válida")

    def _agregar_curso(self):
        print("\n=== NUEVO CURSO ===")
        datos = {
            'id_curso': input("ID: "),
            'id_profesor': input("ID del profesor: "),
            'nombre': input("Nombre del curso: "),
            'id_categoria': input("ID de categoría: "),
            'url_contenido': input("URL de contenido: "),
            'periodo': input("Periodo (1/2): "),
            'precio': input("Precio: "),
            'año': input("Año: "),
            'fecha_inicio': input("Fecha inicio (YYYY-MM-DD): "),
            'fecha_fin': input("Fecha fin (YYYY-MM-DD): ")
        }
        
        if self.operations.insertar_curso(**datos):
            print("✅ Curso registrado exitosamente")

    def _reportes(self):
        while True:
            print("\n=== REPORTES ===")
            print("1. Listar todos los usuarios")
            print("2. Volver")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                usuarios = self.operations.listar_todos_usuarios()
                if usuarios:
                    print(tabulate(usuarios, headers="keys", tablefmt="pretty"))
                else:
                    print("No hay usuarios registrados")
            elif opcion == "2":
                break
            else:
                print("Opción no válida")

    def _validar_genero(self):
        while True:
            genero = input("Género (M/F): ").upper()
            if genero in ['M', 'F']:
                return genero
            print("❌ Debe ser M o F")