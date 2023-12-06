DROP DATABASE OFERTAS_MERCADOLIBRE;
CREATE DATABASE OFERTAS_MERCADOLIBRE;
USE OFERTAS_MERCADOLIBRE;


CREATE TABLE IF NOT EXISTS ofertas_mercado (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(255),
            Precio DECIMAL(10, 2),
            Descuento VARCHAR(50),
            Tipo VARCHAR(50),
            Envio VARCHAR(50)
        );
SELECT * FROM ofertas_mercado;


CREATE OR REPLACE VIEW vista_descuento AS
        SELECT * FROM ofertas_mercado WHERE CAST(descuento AS DECIMAL(5,2)) > 50 ORDER BY CAST(descuento AS DECIMAL(5,2)) DESC;

CREATE OR REPLACE VIEW vista_baratos AS
        SELECT * FROM ofertas_mercado ORDER BY Precio ASC LIMIT 20;
        
CREATE VIEW productosxTipo AS
SELECT Tipo, COUNT(*) AS cantidad_productos
FROM ofertas_mercado
GROUP BY Tipo;
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --- -- -- -- -- -- -- -- -- -- -- -- -- -- --  
CREATE VIEW vista_tipo_envio as select Envio, COUNT(*) as Cantidad FROM ofertas_mercado group by Envio;

CREATE VIEW vista_descuentos AS
SELECT
    CONCAT(FLOOR(descuento / 10) * 10, '% - ', FLOOR(descuento / 10) * 10 + 9, '%') AS rango_descuento,
    COUNT(*) AS cantidad_productos
FROM ofertas_mercado
WHERE descuento >= 10 AND descuento <= 90
GROUP BY rango_descuento
ORDER BY rango_descuento;

SELECT DISTINCT Envio
    FROM
        ofertas_mercado;
        
CREATE VIEW vista_descuentos2 AS
SELECT
    CONCAT(FLOOR(descuento / 10) * 10, '% - ', FLOOR(descuento / 10) * 10 + 9, '%') AS rango_descuento,
    Envio, -- Agregamos el tipo de envío
    COUNT(*) AS cantidad_productos
FROM ofertas_mercado
WHERE descuento >= 10 AND descuento <= 90
GROUP BY rango_descuento, Envio -- Agrupamos también por tipo de envío
ORDER BY rango_descuento, Envio; 

SELECT nombre, precio, Descuento FROM ofertas_mercado;

SELECT Nombre, Precio, Descuento, Tipo FROM ofertas_mercado ORDER BY CAST(Descuento AS DECIMAL(5,2)) DESC LIMIT 5;

SELECT Envio, COUNT(*) as Cantidad_Productos FROM ofertas_mercado GROUP BY Envio;

SELECT Nombre, Precio, Descuento, Tipo FROM ofertas_mercado ORDER BY CAST(Descuento AS DECIMAL(5,2)) ASC LIMIT 10;

CREATE VIEW vista_ofertas_descuento AS
SELECT Descuento, COUNT(*) as Cantidad_Productos
FROM ofertas_mercado
GROUP BY Descuento
ORDER BY CAST(Descuento AS DECIMAL(5,2)) ASC
LIMIT 50;

SELECT * FROM ofertas_mercadolibre.ofertas_mercado;
