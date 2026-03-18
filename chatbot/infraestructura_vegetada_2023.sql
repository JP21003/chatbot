
-- Tabla: definiciones
CREATE TABLE definiciones (
    id INT PRIMARY KEY,
    termino VARCHAR(100),
    definicion TEXT
);

INSERT INTO definiciones (id, termino, definicion) VALUES
(1, 'Jardín vertical', 'Cobertura vegetal con plantas herbáceas, epífitas, bejucos o enredaderas que se instalan sobre muros u otras superficies verticales para beneficios ambientales y paisajísticos.');

-- Tabla: fuentes_adicionales
CREATE TABLE fuentes_adicionales (
    id INT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion TEXT,
    enlace TEXT
);

INSERT INTO fuentes_adicionales (id, nombre, descripcion, enlace) VALUES
(1, 'Guía de Especies Vegetales', 'Documento de la Secretaría Distrital de Ambiente con especies recomendadas para techos verdes y jardines verticales.', 'https://www.ambientebogota.gov.co/es/techos-verdes-y-jardines-verticales'),
(2, 'Guía de agricultura urbana 2023', 'Guía complementaria sobre prácticas de agricultura urbana.', 'https://www.ambientebogota.gov.co/es/techos-verdes-y-jardines-verticales');

-- Tabla: autores
CREATE TABLE autores (
    id INT PRIMARY KEY,
    nombre VARCHAR(100)
);

INSERT INTO autores (id, nombre) VALUES
(1, 'Alejandro Gómez Cubillos'),
(2, 'Diana Carolina Mora'),
(3, 'José Fernando Cuello');
