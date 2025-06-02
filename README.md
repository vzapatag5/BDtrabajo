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
 Implementación de sistema académico para la plataforma NODO de la Universidad EAFIT, que permite la creación y administración de cursos, matricular estudiantes, gestión de usuarios, publicación de materiales y tareas, así como también la participación activa en foros, ofreciendo diferentes funcionalidades según su rol.
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

bases de datos cerradas cada que se hace uan transaccion se cierra la bd
#
## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

### como se compila y ejecuta.
 se compila desde consola ejecutando desde el archivo main.py
### detalles del desarrollo.
 el lenguaje utilizado fue Python, y el motor de base de datos sistema_nodo es MYSQL con el software XAMPP
### detalles técnicos
 
### descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## 
## opcionalmente - si quiere mostrar resultados o pantallazos 

## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## IP o nombres de dominio en nube o en la máquina servidor.
localhost:3306 (dependiendo de la configuracion de MYSQL de cada computador)

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
 se ejecuta por consola con el comando python main.py, base de datos sistema_nodo.sql, y está dividido en 2 partes: backend y frontend.
## como se lanza el servidor.
 ejecuto main.py
## una mini guia de como un usuario utilizaría el software o la aplicación
    
## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## sitio2-url
## url de donde tomo info para desarrollar este proyecto
