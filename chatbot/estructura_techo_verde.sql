
-- Tabla: secciones
CREATE TABLE secciones (
    id INT PRIMARY KEY,
    titulo VARCHAR(255),
    descripcion TEXT
);

INSERT INTO secciones (id, titulo, descripcion) VALUES
(1, 'Introducción', 'Presenta el contexto y justificación de los techos verdes y jardines verticales.'),
(2, 'Techos verdes', 'Describe los tipos, componentes y recomendaciones para techos verdes.'),
(3, 'Jardines verticales', 'Incluye definiciones, sistemas y cuidados de jardines verticales.'),
(4, 'Consideraciones técnicas', 'Requisitos estructurales, hidráulicos, y vegetales para implementación.');

-- Tabla: terminos
CREATE TABLE terminos (
    id INT PRIMARY KEY,
    termino VARCHAR(100),
    definicion TEXT
);

INSERT INTO terminos (id, termino, definicion) VALUES
(1, 'Techo Verde', 'Sistema instalado sobre la cubierta de un edificio que incluye vegetación.'),
(2, 'Jardín Vertical', 'Sistema que permite cultivar plantas verticalmente en muros o fachadas.'),
(3, 'Sustrato', 'Medio de crecimiento para las plantas que reemplaza al suelo.');

-- Tabla: sistemas_verdes
CREATE TABLE sistemas_verdes (
    id INT PRIMARY KEY,
    tipo VARCHAR(100),
    descripcion TEXT,
    categoria VARCHAR(50)
);

INSERT INTO sistemas_verdes (id, tipo, descripcion, categoria) VALUES
(1, 'Extensivo', 'Techo verde de bajo peso y mantenimiento', 'Techo Verde'),
(2, 'Intensivo', 'Techo verde con mayor profundidad de sustrato', 'Techo Verde'),
(3, 'Sistema modular', 'Jardín vertical conformado por módulos independientes', 'Jardín Vertical');

-- Tabla: componentes
CREATE TABLE componentes (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    funcion TEXT,
    aplica_a VARCHAR(50)
);

INSERT INTO componentes (id, nombre, funcion, aplica_a) VALUES
(1, 'Membrana impermeabilizante', 'Evita filtraciones de agua', 'Ambos'),
(2, 'Capa de drenaje', 'Permite evacuar el exceso de agua', 'Techo Verde'),
(3, 'Sistema de riego', 'Proporciona agua a las plantas', 'Ambos');

-- Tabla: requisitos
CREATE TABLE requisitos (
    id INT PRIMARY KEY,
    tema VARCHAR(100),
    detalle TEXT,
    tipo_requisito VARCHAR(50)
);

INSERT INTO requisitos (id, tema, detalle, tipo_requisito) VALUES
(1, 'Carga estructural', 'La estructura debe soportar el peso del sistema verde.', 'Estructural'),
(2, 'Acceso y mantenimiento', 'Debe existir un acceso seguro para mantenimiento.', 'Operativo'),
(3, 'Evacuación de aguas', 'Debe garantizarse el drenaje y control de escorrentía.', 'Hidráulico');

-- Tabla: beneficios
CREATE TABLE beneficios (
    id INT PRIMARY KEY,
    tipo VARCHAR(50),
    descripcion TEXT
);

INSERT INTO beneficios (id, tipo, descripcion) VALUES
(1, 'Ambiental', 'Reducción del efecto isla de calor y mejora de calidad del aire.'),
(2, 'Económico', 'Disminución del consumo energético por aislamiento térmico.'),
(3, 'Social', 'Contribuye al bienestar y mejora el paisaje urbano.');

-- Tabla: normativas
CREATE TABLE normativas (
    id INT PRIMARY KEY,
    codigo VARCHAR(50),
    descripcion TEXT,
    aplica_a VARCHAR(100)
);

INSERT INTO normativas (id, codigo, descripcion, aplica_a) VALUES
(1, 'NSR-10', 'Norma Colombiana de Construcción Sismo Resistente', 'Estructura soporte'),
(2, 'RAS 2000', 'Reglamento Técnico del Sector de Agua Potable y Saneamiento Básico', 'Sistemas de drenaje');
