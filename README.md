# info de la materia: <S2561-0701> <Bases de datos>
#
# Estudiante(s): 
# Mariana Carrasquilla, mcarrasqub@eafit.edu.co
# Valentina Zapata, vzapatag5@eafit.edu.co
# Jerónimo Restrepo, jrestrepg1@eafit.edu.co       
#
# Profesor: Edwin Nelson Montoya, emontoya@eafit.edu.co
#

# Sistema Académico - Gestión de Cursos, Estudiantes y Profesores
#
# 1. breve descripción de la actividad
# El sistema académico es una aplicación de consola desarrollada en Python que permite gestionar cursos, estudiantes y profesores en una institución educativa. El sistema ofrece diferentes funcionalidades según el rol del usuario (administrador, profesor o estudiante), incluyendo gestión de cursos, materiales, foros y tareas.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
# Validación de datos antes de inserción en la base de datos
# Separación de roles y permisos
# Código modularizado por funcionalidades
# bases de datos cerradas cada que se hace uan transaccion se cierra la bd

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Tecnologías utilizadas:

Python 3.9+

MySQL 8.0+

XAMPP 3.3.0 (para servidor MySQL local)

## como se compila y ejecuta.
 se compila desde consola ejecutando desde el archivo main.py
## detalles del desarrollo.
 el lenguaje utilizado fue Python, y el motor de base de datos sistema_nodo es MYSQL con el software XAMPP
## detalles técnicos
 
## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

# .
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
## opcionalmente - si quiere mostrar resultados o pantallazos 

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.
localhost:3306 (dependiendo de la configuracion de MYSQL de cada computador)

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
 se ejecuta por consola con el comando python main.py, base de datos sistema_nodo.sql, y está dividido en 2 partes: backend y frontend.
## como se lanza el servidor.
 ejecuto main.py
## una mini guia de como un usuario utilizaría el software o la aplicación
Guía de usuario:

Instalar MySQL (o XAMPP si es local).

Crear la base de datos sistema_nodo.

Configurar el archivo db.py con sus credenciales.

Ejecutar python main.py (el sistema detectará automáticamente la configuración).
Iniciar la aplicación

Ingresar con username y password

Navegar por los menús según su rol

Seleccionar opciones numéricas para realizar acciones

Seguir las instrucciones en pantalla para cada operación

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.
El sistema fue desarrollado como proyecto final para el curso de Bases de Datos, implementando los conceptos aprendidos sobre diseño de bases de datos relacionales y programación con Python.
# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/ 
## sitio2-https://www.freecodecamp.org/news/connect-python-with-sql/ 
## url de donde tomo info para desarrollar este proyecto
