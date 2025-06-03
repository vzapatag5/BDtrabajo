# info de la materia: Código S2561-0701, Bases de datos
#
## Estudiantes: 
### Mariana Carrasquilla, mcarrasqub@eafit.edu.co
### Valentina Zapata, vzapatag5@eafit.edu.co
### Jerónimo Restrepo, jrestrepg1@eafit.edu.co       
#
## Profesor: 
### Edwin Nelson Montoya, emontoya@eafit.edu.co
#
# Sistema Académico - Gestión de Cursos, Estudiantes y Profesores
#
## 1. breve descripción de la actividad
Implementación de sistema académico para la plataforma NODO de la Universidad EAFIT, que permite la creación y administración de cursos, matricular estudiantes, gestión de usuarios, publicación de materiales y tareas, así como también la participación activa en foros, ofreciendo diferentes funcionalidades según el rol (profesor, admin, estudiante).
#
### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Se cumplió con el desarrollo delmodelo Entidad-Relación, modelo relacional normalizado, la implementación física en MySQL, consultas SQL variadas y una aplicación en python donde se evidencia:

 * Autenticación por Roles.
 * Gestión de cursos.
 * Publicación de materiales y tareas.
 * Sistema de foros completo.
 * Reportes administrativos.

### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

No se realizó una interfaz gráfica como originalmente se propuso y se mantuvo todo el funcionamiento por consola.
#
## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Bases de datos: cerradas cada que se hace una transacción se cierra la base de datos.

* Validación de datos antes de inserción en la base de datos.

* Separación de roles y permisos.

* Código modularizado por funcionalidades.
#
## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

### a) ¿Como se compila y ejecuta?
Asegurese de tener Python 3.8+ instalado:
```bash
python --version 
```
Asegurese de instalar en VS Code las siguientes librerías:
```bash
pip install pymysql tabulate
```
 Se compila desde consola ejecutando desde el archivo main.py.
 #
### b) Detalles del desarrollo
 el lenguaje utilizado fue Python, y el motor de base de datos sistema_nodo es MYSQL con el software XAMPP o WORKBENCH.

#
### Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
Asegurese de poner la información de su conexión correctamente en db.py en la parte:
```bash
host="localhost",
user="root",
port=3307, # revisar su puerto
password="", #ponga su contraseña si la tiene
database="sistema_nodo",
cursorclass=DictCursor,
autocommit=False
```
#
### Detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

# 
├── main.py            # Punto de entrada de la aplicación

├── README.md          # Documentación del proyecto 

├── backend/           # Lógica de negocio y acceso a datos

│   ├── auth.py        # Autenticación de usuarios

│   ├── admin.py       # backend admin

│   ├── profesor.py    # backend profesor

│   ├── db.py          # Conexión a la base de datos

│   └── estudiante.py  # backend estudiante

└── frontend/          # Interfaz de usuario

│   ├── admin.py       # Interfaz gráfica admin

│   ├── profesor.py    # Interfaz gráfica admin

│   ├── main_ui.py     # main frontend

│   └── estudiante.py  # Interfaz gráfica estudiante
#
## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
#
### a) IP o nombres de dominio en nube o en la máquina servidor.
localhost:3306 (dependiendo de la configuracion de MYSQL de cada computador)
#
### b) Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
 se ejecuta por consola con el comando python main.py, base de datos sistema_nodo.sql, y está dividido en 2 partes: backend y frontend.
 #
### c) Guía de usuario:

* Instalar MySQL (WORKBENCH o XAMPP si es local).

* Crear la base de datos sistema_nodo.

* Configurar el archivo db.py con sus credenciales.

* Ejecutar python main.py (el sistema detectará automáticamente la configuración).

* Iniciar la aplicación.

* Ingresar al sistema con username y password.

* Navegar por los menús según su rol.

* Seleccionar opciones numéricas para realizar acciones.

* Seguir las instrucciones en pantalla para cada operación.
#
## 5. otra información que considere relevante para esta actividad.
El sistema fue desarrollado como proyecto final para el curso de Bases de Datos, implementando los conceptos aprendidos sobre diseño de bases de datos relacionales y programación con Python.
#
## referencias:
## sitio1-https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/ 
## sitio2-https://www.freecodecamp.org/news/connect-python-with-sql/ 
## sitio3-https://pymysql.readthedocs.io/
