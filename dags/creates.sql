CREATE TABLE IF NOT EXISTS location (
        id INT PRIMARY KEY,
        nombre VARCHAR(100)
    ) DISTSTYLE ALL SORTKEY (id);
    INSERT INTO location (id, nombre)
    VALUES
        (1, 'Buenos Aires'),
        (2, 'Córdoba'),
        (3, 'Rosario'),
        (4, 'Mendoza'),
        (5, 'San Miguel de Tucumán'),
        (6, 'La Plata'),
        (7, 'Mar del Plata'),
        (8, 'Salta'),
        (9, 'Santa Fe'),
        (10, 'San Juan'),
        (11, 'Resistencia'),
        (12, 'Santiago del Estero'),
        (13, 'Posadas'),
        (14, 'San Salvador de Jujuy'),
        (15, 'Bahía Blanca'),
        (16, 'Paraná'),
        (17, 'Merlo'),
        (18, 'José C. Paz'),
        (19, 'Quilmes'),
        (20, 'Pilar');

CREATE TABLE IF NOT EXISTS forecast (
        id INT IDENTITY(1,1) PRIMARY KEY,
        date TIMESTAMP,
        prediction_date TIMESTAMP,
        locationId INT REFERENCES location(id),
        max_temperature FLOAT,
        min_temperature FLOAT,
        precipitation_probability_max FLOAT
    ) DISTKEY (locationId) SORTKEY (date);