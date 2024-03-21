CREATE TABLE IF NOT EXISTS forecast (
        id INT IDENTITY(1,1) PRIMARY KEY,
        date TIMESTAMP,
        prediction_date TIMESTAMP,
        locationId INT REFERENCES location(id),
        max_temperature FLOAT,
        min_temperature FLOAT,
        precipitation_probability_max FLOAT
    ) DISTKEY (locationId) SORTKEY (date);