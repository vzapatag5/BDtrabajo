-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-05-2025 a las 04:38:29
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sistema_nodo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `adminis`
--
CREATE DATABASE sistema_nodo;
USE sistema_nodo;
CREATE TABLE `adminis` (
  `id_admin` int(12) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `genero` char(1) NOT NULL,
  `contrasena` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `adminis`
--

INSERT INTO `adminis` (`id_admin`, `nombre`, `email`, `genero`, `contrasena`) VALUES
(1024755032, 'Carlos Perez', 'cperez@eafit.com', 'M', '712*');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignacion_tarea`
--

CREATE TABLE `asignacion_tarea` (
  `id_tarea` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `id_profesor` int(12) NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `desc_tarea` varchar(200) NOT NULL,
  `nombre_archivo` varchar(100) NOT NULL,
  `fecha_creacion_tarea` date NOT NULL,
  `fecha_entrega_tarea` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asignacion_tarea`
--

INSERT INTO `asignacion_tarea` (`id_tarea`, `id_curso`, `id_profesor`, `nombre`, `desc_tarea`, `nombre_archivo`, `fecha_creacion_tarea`, `fecha_entrega_tarea`) VALUES
(1, 1, 102573365, 'Tarea 1 - Modelo ER', 'Diseñar modelo para biblioteca', 'tarea1.pdf', '2025-01-29', '2025-02-12'),
(2, 2, 701763359, 'Tarea 1: Comandos Linux', 'Ejercicios con terminal', 'trabajo1.pdf', '2025-01-22', '2025-02-15'),
(3, 3, 700443790, 'Tarea 1: Interés y descuento', 'Ejercicios con interés', 'entrega1.pdf', '2025-01-24', '2025-02-16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asig_profecurso`
--

CREATE TABLE `asig_profecurso` (
  `id_asignacion` int(11) NOT NULL,
  `id_admin` int(12) NOT NULL,
  `id_profesor` int(12) NOT NULL,
  `id_curso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asig_profecurso`
--

INSERT INTO `asig_profecurso` (`id_asignacion`, `id_admin`, `id_profesor`, `id_curso`) VALUES
(1, 1024755032, 102573365, 1),
(2, 1024755032, 700443790, 3),
(3, 1024755032, 701763359, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id_categoria`, `nombre`) VALUES
(1, 'Ciencias aplicadas e ingeniería'),
(2, 'Administración');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `creacion_foro`
--

CREATE TABLE `creacion_foro` (
  `id_foro` int(11) NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `id_profesor` int(12) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `desc_foro` varchar(200) NOT NULL,
  `fecha_creacion_foro` date NOT NULL,
  `fecha_termin_foro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `creacion_foro`
--

INSERT INTO `creacion_foro` (`id_foro`, `nombre`, `id_profesor`, `id_curso`, `desc_foro`, `fecha_creacion_foro`, `fecha_termin_foro`) VALUES
(1, 'Dudas generales', 102573365, 1, 'Espacio para preguntas', '2025-02-20', '2025-07-01'),
(2, 'Tarea 1', 701763359, 2, 'Consultas sobre la tarea', '2025-02-22', '2025-07-01'),
(3, 'Entrega 1', 700443790, 3, 'Inquietudes sobre trabajo', '2025-02-23', '2025-07-01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `curso`
--

CREATE TABLE `curso` (
  `id_curso` int(11) NOT NULL,
  `id_profesor` int(12) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `url_contenido` varchar(600) NOT NULL,
  `periodo` int(1) NOT NULL,
  `precio` int(99) NOT NULL,
  `año` int(10) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `curso`
--

INSERT INTO `curso` (`id_curso`, `id_profesor`, `nombre`, `id_categoria`, `url_contenido`, `periodo`, `precio`, `año`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 102573365, 'Bases de datos', 1, 'cursobd.com', 1, 500000, 2025, '2025-01-20', '2025-07-01'),
(2, 701763359, 'Sistemas operativos', 1, 'curso1.com', 1, 750000, 2025, '2025-01-20', '2025-07-01'),
(3, 700443790, 'Financieras', 2, 'cursomut.com', 1, 500000, 2025, '2025-01-20', '2025-07-01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrega_tarea`
--

CREATE TABLE `entrega_tarea` (
  `id_entrega` int(11) NOT NULL,
  `id_tarea` int(11) NOT NULL,
  `id_estudiante` int(12) NOT NULL,
  `calificacion` float(2,1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entrega_tarea`
--

INSERT INTO `entrega_tarea` (`id_entrega`, `id_tarea`, `id_estudiante`, `calificacion`) VALUES
(1, 1, 1034988632, 5.0),
(2, 1, 1034988632, 4.0),
(3, 2, 1034755213, 5.0),
(4, 3, 1025619334, 5.0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE `estudiante` (
  `id_estudiante` int(12) NOT NULL,
  `id_nodo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `genero` char(1) NOT NULL,
  `contrasena` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiante`
--

INSERT INTO `estudiante` (`id_estudiante`, `id_nodo`, `nombre`, `email`, `genero`, `contrasena`) VALUES
(1025619334, 3, 'Carlos Martinez', 'cmartinez@eafit.com', 'M', '789+'),
(1025762685, 4, 'Valentina Zapata', 'vzapata@eafit.com', 'F', '4567+'),
(1034755213, 2, 'Bridgitte López', 'blopez@eafit.com', 'F', '456*'),
(1034988632, 1, 'Maria Acosta', 'macosta@eafit.com', 'F', '123*');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `foro_usuario`
--

CREATE TABLE `foro_usuario` (
  `id_registro` int(11) NOT NULL,
  `id_foro` int(11) NOT NULL,
  `id_estudiante` int(12) DEFAULT NULL,
  `id_profesor` int(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `foro_usuario`
--

INSERT INTO `foro_usuario` (`id_registro`, `id_foro`, `id_estudiante`, `id_profesor`) VALUES
(1, 1, 1034988632, NULL),
(2, 1, NULL, 102573365),
(3, 1, 1025619334, NULL),
(4, 2, 1034988632, NULL),
(5, 2, NULL, 701763359),
(6, 3, 1034755213, NULL),
(7, 3, NULL, 700443790);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `material`
--

CREATE TABLE `material` (
  `id_material` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `desc_material` varchar(200) NOT NULL,
  `nombre_archivo` varchar(100) NOT NULL,
  `fecha_public` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `material`
--

INSERT INTO `material` (`id_material`, `id_curso`, `titulo`, `desc_material`, `nombre_archivo`, `fecha_public`) VALUES
(1, 1, 'Guía SQL Avanzado', 'Ejercicios prácticos de SQL', 'guia_sql.pdf', '2025-02-20'),
(2, 2, 'Introducción a Linux', 'Conceptos básicos de Linux', 'intro_linux.pdf', '2025-03-10'),
(3, 3, 'Introducción', 'Conceptos básicos del valor del dinero', 'intro_interés.pdf', '2025-02-22');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matricula`
--

CREATE TABLE `matricula` (
  `id_matricula` int(11) NOT NULL,
  `id_pago` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `fecha_matricula` date NOT NULL,
  `semestre` int(11) NOT NULL,
  `año` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `matricula`
--

INSERT INTO `matricula` (`id_matricula`, `id_pago`, `id_curso`, `fecha_matricula`, `semestre`, `año`) VALUES
(1, 1, 1, '2025-01-18', 2, 2025),
(2, 2, 2, '2025-01-18', 2, 2025),
(3, 3, 3, '2025-01-19', 1, 2025),
(4, 4, 1, '2025-01-18', 2, 2025);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensaje_foro`
--

CREATE TABLE `mensaje_foro` (
  `id_mensaje` int(11) NOT NULL,
  `id_estudiante` int(12) DEFAULT NULL,
  `id_profesor` int(12) DEFAULT NULL,
  `id_foro` int(11) NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `desc_msj_foro` varchar(200) NOT NULL,
  `fecha_envio` date NOT NULL,
  `id_mensaje_respuesta` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensaje_foro`
--

INSERT INTO `mensaje_foro` (`id_mensaje`, `id_estudiante`, `id_profesor`, `id_foro`, `nombre`, `desc_msj_foro`, `fecha_envio`, `id_mensaje_respuesta`) VALUES
(1, NULL, 102573365, 1, 'Bienvenida', 'Bienvenidos al curso', '2025-02-10', NULL),
(2, 1034988632, NULL, 1, 'Respuesta', 'Gracias profesor', '2025-02-11', 1),
(3, 1034988632, NULL, 2, 'Consulta material', '¿Dónde estén los materiales', '2025-02-12', NULL),
(4, 1034755213, NULL, 3, 'Consulta tarea', '¿Cuales son los requisitos?', '2025-02-13', NULL),
(5, 1025619334, NULL, 1, 'Respuesta', 'Muchas gracias profesor', '2025-02-12', 1),
(6, NULL, 700443790, 3, 'Respuesta requisites', 'Mis adelante les publico las requisitos', '2025-02-14', 4),
(7, NULL, 701763359, 2, 'Respuesta consulta material', 'En la parte de archivos de grupo', '2025-02-12', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago`
--

CREATE TABLE `pago` (
  `id_pago` int(11) NOT NULL,
  `id_estudiante` int(12) NOT NULL,
  `valor_pago` int(11) NOT NULL,
  `comprobante` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pago`
--

INSERT INTO `pago` (`id_pago`, `id_estudiante`, `valor_pago`, `comprobante`) VALUES
(1, 1034988632, 500000, 'REF-001'),
(2, 1034988632, 750000, 'REF-002'),
(3, 1034755213, 750000, 'REF-003'),
(4, 1025619334, 500000, 'REF-004');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesor`
--

CREATE TABLE `profesor` (
  `id_profesor` int(20) NOT NULL,
  `area_principal` varchar(100) NOT NULL,
  `area_alternativa` varchar(100) DEFAULT NULL,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `genero` char(1) NOT NULL,
  `contrasena` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesor`
--

INSERT INTO `profesor` (`id_profesor`, `area_principal`, `area_alternativa`, `nombre`, `email`, `genero`, `contrasena`) VALUES
(102573365, 'Sistemas', NULL, 'Julian Gomez', 'jgomez@eafit.com', 'M', '342+'),
(700443790, 'Finanzas', 'Matemática', 'Lorena Correa', 'lcorrea@eafit.com', 'F', '198*'),
(701763359, 'Sistemas', 'Matemática', 'Andrea Torres', 'atorres@eafit.com', 'F', '202+');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `adminis`
--
ALTER TABLE `adminis`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indices de la tabla `asignacion_tarea`
--
ALTER TABLE `asignacion_tarea`
  ADD PRIMARY KEY (`id_tarea`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_profesor` (`id_profesor`);

--
-- Indices de la tabla `asig_profecurso`
--
ALTER TABLE `asig_profecurso`
  ADD PRIMARY KEY (`id_asignacion`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_admin` (`id_admin`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `creacion_foro`
--
ALTER TABLE `creacion_foro`
  ADD PRIMARY KEY (`id_foro`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indices de la tabla `curso`
--
ALTER TABLE `curso`
  ADD PRIMARY KEY (`id_curso`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indices de la tabla `entrega_tarea`
--
ALTER TABLE `entrega_tarea`
  ADD PRIMARY KEY (`id_entrega`),
  ADD KEY `id_tarea` (`id_tarea`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD PRIMARY KEY (`id_estudiante`);

--
-- Indices de la tabla `foro_usuario`
--
ALTER TABLE `foro_usuario`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_foro` (`id_foro`),
  ADD KEY `id_profesor` (`id_profesor`);

--
-- Indices de la tabla `material`
--
ALTER TABLE `material`
  ADD PRIMARY KEY (`id_material`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indices de la tabla `matricula`
--
ALTER TABLE `matricula`
  ADD PRIMARY KEY (`id_matricula`),
  ADD KEY `id_pago` (`id_pago`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indices de la tabla `mensaje_foro`
--
ALTER TABLE `mensaje_foro`
  ADD PRIMARY KEY (`id_mensaje`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_foro` (`id_foro`);

--
-- Indices de la tabla `pago`
--
ALTER TABLE `pago`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `profesor`
--
ALTER TABLE `profesor`
  ADD PRIMARY KEY (`id_profesor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asignacion_tarea`
--
ALTER TABLE `asignacion_tarea`
  MODIFY `id_tarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `asig_profecurso`
--
ALTER TABLE `asig_profecurso`
  MODIFY `id_asignacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `creacion_foro`
--
ALTER TABLE `creacion_foro`
  MODIFY `id_foro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `curso`
--
ALTER TABLE `curso`
  MODIFY `id_curso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `entrega_tarea`
--
ALTER TABLE `entrega_tarea`
  MODIFY `id_entrega` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `foro_usuario`
--
ALTER TABLE `foro_usuario`
  MODIFY `id_registro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `material`
--
ALTER TABLE `material`
  MODIFY `id_material` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `matricula`
--
ALTER TABLE `matricula`
  MODIFY `id_matricula` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `pago`
--
ALTER TABLE `pago`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asignacion_tarea`
--
ALTER TABLE `asignacion_tarea`
  ADD CONSTRAINT `asignacion_tarea_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`),
  ADD CONSTRAINT `asignacion_tarea_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id_profesor`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `asig_profecurso`
--
ALTER TABLE `asig_profecurso`
  ADD CONSTRAINT `asig_profecurso_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id_profesor`),
  ADD CONSTRAINT `asig_profecurso_ibfk_2` FOREIGN KEY (`id_admin`) REFERENCES `adminis` (`id_admin`),
  ADD CONSTRAINT `asig_profecurso_ibfk_3` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `creacion_foro`
--
ALTER TABLE `creacion_foro`
  ADD CONSTRAINT `creacion_foro_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id_profesor`),
  ADD CONSTRAINT `creacion_foro_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `curso`
--
ALTER TABLE `curso`
  ADD CONSTRAINT `curso_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id_profesor`),
  ADD CONSTRAINT `curso_ibfk_2` FOREIGN KEY (`id_categoria`) REFERENCES `categoria` (`id_categoria`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `entrega_tarea`
--
ALTER TABLE `entrega_tarea`
  ADD CONSTRAINT `entrega_tarea_ibfk_1` FOREIGN KEY (`id_tarea`) REFERENCES `asignacion_tarea` (`id_tarea`),
  ADD CONSTRAINT `entrega_tarea_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `foro_usuario`
--
ALTER TABLE `foro_usuario`
  ADD CONSTRAINT `foro_usuario_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`),
  ADD CONSTRAINT `foro_usuario_ibfk_2` FOREIGN KEY (`id_foro`) REFERENCES `creacion_foro` (`id_foro`),
  ADD CONSTRAINT `foro_usuario_ibfk_3` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id_profesor`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `material`
--
ALTER TABLE `material`
  ADD CONSTRAINT `material_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `matricula`
--
ALTER TABLE `matricula`
  ADD CONSTRAINT `matricula_ibfk_1` FOREIGN KEY (`id_pago`) REFERENCES `pago` (`id_pago`) ON UPDATE CASCADE,
  ADD CONSTRAINT `matricula_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `mensaje_foro`
--
ALTER TABLE `mensaje_foro`
  ADD CONSTRAINT `mensaje_foro_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`),
  ADD CONSTRAINT `mensaje_foro_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id_profesor`),
  ADD CONSTRAINT `mensaje_foro_ibfk_3` FOREIGN KEY (`id_foro`) REFERENCES `creacion_foro` (`id_foro`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `pago`
--
ALTER TABLE `pago`
  ADD CONSTRAINT `pago_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
