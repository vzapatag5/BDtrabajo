CREATE DATABASE IF NOT EXISTS sistema_nodo;
USE sistema_nodo;

-- procedures.sql
DELIMITER //

-- =============================================
-- PROCEDIMIENTOS DE AUTENTICACIÓN
-- =============================================

CREATE PROCEDURE sp_login_admin(
    IN p_email VARCHAR(50),
    IN p_contrasena VARCHAR(20)
)
BEGIN
    SELECT id_admin AS id, nombre, email, genero 
    FROM adminis 
    WHERE email = p_email AND contrasena = p_contrasena;
END //

CREATE PROCEDURE sp_login_profesor(
    IN p_email VARCHAR(50),
    IN p_contrasena VARCHAR(20)
)
BEGIN
    SELECT id_profesor AS id, nombre, email, genero 
    FROM profesor 
    WHERE email = p_email AND contrasena = p_contrasena;
END //

CREATE PROCEDURE sp_login_estudiante(
    IN p_email VARCHAR(50),
    IN p_contrasena VARCHAR(20)
)
BEGIN
    SELECT id_estudiante AS id, nombre, email, genero 
    FROM estudiante 
    WHERE email = p_email AND contrasena = p_contrasena;
END //

-- =============================================
-- PROCEDIMIENTOS PARA ADMINISTRADOR
-- =============================================

CREATE PROCEDURE sp_insertar_estudiante(
    IN p_id_estudiante INT,
    IN p_id_nodo INT,
    IN p_nombre VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_genero CHAR(1),
    IN p_contrasena VARCHAR(20)
)
BEGIN
    INSERT INTO estudiante (id_estudiante, id_nodo, nombre, email, genero, contrasena)
    VALUES (p_id_estudiante, p_id_nodo, p_nombre, p_email, p_genero, p_contrasena);
END //

CREATE PROCEDURE sp_insertar_profesor(
    IN p_id_profesor INT,
    IN p_area_principal VARCHAR(100),
    IN p_area_alternativa VARCHAR(100),
    IN p_nombre VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_genero CHAR(1),
    IN p_contrasena VARCHAR(20)
)
BEGIN
    INSERT INTO profesor (id_profesor, area_principal, area_alternativa, nombre, email, genero, contrasena)
    VALUES (p_id_profesor, p_area_principal, p_area_alternativa, p_nombre, p_email, p_genero, p_contrasena);
END //

CREATE PROCEDURE sp_insertar_curso(
    IN p_id_curso INT,
    IN p_id_profesor INT,
    IN p_nombre VARCHAR(30),
    IN p_id_categoria INT,
    IN p_url_contenido VARCHAR(600),
    IN p_periodo INT,
    IN p_precio INT,
    IN p_anio INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    INSERT INTO curso (id_curso, id_profesor, nombre, id_categoria, url_contenido, periodo, precio, anio, fecha_inicio, fecha_fin)
    VALUES (p_id_curso, p_id_profesor, p_nombre, p_id_categoria, p_url_contenido, p_periodo, p_precio, p_anio, p_fecha_inicio, p_fecha_fin);
END //

CREATE PROCEDURE sp_listar_estudiantes()
BEGIN
    SELECT id_estudiante, id_nodo, nombre, email, genero FROM estudiante;
END //

CREATE PROCEDURE sp_listar_profesores()
BEGIN
    SELECT id_profesor, area_principal, area_alternativa, nombre, email, genero FROM profesor;
END //

CREATE PROCEDURE sp_listar_cursos()
BEGIN
    SELECT c.id_curso, c.nombre, p.nombre AS profesor, cat.nombre AS categoria
    FROM curso c
    JOIN profesor p ON c.id_profesor = p.id_profesor
    JOIN categoria cat ON c.id_categoria = cat.id_categoria;
END //

-- =============================================
-- PROCEDIMIENTOS PARA PROFESOR
-- =============================================

CREATE PROCEDURE sp_publicar_tarea(
    IN p_id_tarea INT,
    IN p_id_curso INT,
    IN p_id_profesor INT,
    IN p_nombre VARCHAR(70),
    IN p_desc_tarea VARCHAR(200),
    IN p_nombre_archivo VARCHAR(100),
    IN p_fecha_creacion DATE,
    IN p_fecha_entrega DATE
)
BEGIN
    INSERT INTO asignacion_tarea (id_tarea, id_curso, id_profesor, nombre, desc_tarea, nombre_archivo, fecha_creacion_tarea, fecha_entrega_tarea)
    VALUES (p_id_tarea, p_id_curso, p_id_profesor, p_nombre, p_desc_tarea, p_nombre_archivo, p_fecha_creacion, p_fecha_entrega);
END //

CREATE PROCEDURE sp_listar_cursos_profesor(IN p_id_profesor INT)
BEGIN
    SELECT c.id_curso, c.nombre, cat.nombre AS categoria
    FROM curso c
    JOIN categoria cat ON c.id_categoria = cat.id_categoria
    WHERE c.id_profesor = p_id_profesor;
END //

CREATE PROCEDURE sp_listar_estudiantes_curso(IN p_id_curso INT)
BEGIN
    SELECT e.id_estudiante, e.nombre, e.email
    FROM estudiante e
    JOIN matricula m ON e.id_estudiante = m.id_estudiante
    WHERE m.id_curso = p_id_curso;
END //

CREATE PROCEDURE sp_publicar_material(
    IN p_id_material INT,
    IN p_id_curso INT,
    IN p_id_profesor INT,
    IN p_titulo VARCHAR(100),
    IN p_desc_material VARCHAR(200),
    IN p_nombre_archivo VARCHAR(100),
    IN p_fecha_public DATE
)
BEGIN
    INSERT INTO material (id_material, id_curso, id_profesor, titulo, desc_material, nombre_archivo, fecha_public)
    VALUES (p_id_material, p_id_curso, p_id_profesor, p_titulo, p_desc_material, p_nombre_archivo, p_fecha_public);
END //

-- =============================================
-- PROCEDIMIENTOS PARA ESTUDIANTE
-- =============================================

CREATE PROCEDURE sp_descargar_material(IN p_id_material INT)
BEGIN
    SELECT titulo, desc_material, nombre_archivo 
    FROM material 
    WHERE id_material = p_id_material;
END //

CREATE PROCEDURE sp_listar_tareas_estudiante(IN p_id_estudiante INT)
BEGIN
    SELECT at.id_tarea, c.nombre AS curso, at.nombre, at.desc_tarea, 
           at.fecha_entrega_tarea AS fecha_entrega
    FROM asignacion_tarea at
    JOIN curso c ON at.id_curso = c.id_curso
    JOIN matricula m ON c.id_curso = m.id_curso
    WHERE m.id_estudiante = p_id_estudiante;
END //

CREATE PROCEDURE sp_listar_respuestas_foro(IN p_id_foro INT)
BEGIN
    SELECT mf.id_mensaje, 
           COALESCE(e.nombre, p.nombre) AS autor,
           mf.desc_msj_foro AS mensaje,
           mf.fecha_envio AS fecha
    FROM mensaje_foro mf
    LEFT JOIN estudiante e ON mf.id_estudiante = e.id_estudiante
    LEFT JOIN profesor p ON mf.id_profesor = p.id_profesor
    WHERE mf.id_foro = p_id_foro;
END //

CREATE PROCEDURE sp_responder_foro(
    IN p_id_foro INT,
    IN p_id_estudiante INT,
    IN p_mensaje VARCHAR(200)
)
BEGIN
    DECLARE next_id INT;
    
    SELECT IFNULL(MAX(id_mensaje), 0) + 1 INTO next_id FROM mensaje_foro;
    
    INSERT INTO mensaje_foro (id_mensaje, id_estudiante, id_foro, 
                             nombre, desc_msj_foro, fecha_envio)
    VALUES (next_id, p_id_estudiante, p_id_foro, 
            'Respuesta estudiante', p_mensaje, CURDATE());
END //

DELIMITER ;