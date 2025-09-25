DROP TABLE IF EXISTS delta.reading
GO
DROP TABLE IF EXISTS delta.plant
GO
DROP TABLE IF EXISTS delta.country
GO
DROP TABLE IF EXISTS delta.city
GO
DROP TABLE IF EXISTS delta.species
GO
DROP TABLE IF EXISTS delta.botanist
GO

CREATE TABLE delta.country (
    country_id int IDENTITY(1,1) PRIMARY KEY,
    country_name varchar(255) UNIQUE
)
GO

CREATE TABLE delta.city (
    city_id int IDENTITY(1,1) PRIMARY KEY,
    city_name varchar(255) UNIQUE
)
GO

CREATE TABLE delta.species (
    species_id int IDENTITY(1,1) PRIMARY KEY,
    species_name varchar(255) UNIQUE
)

CREATE TABLE delta.botanist (
    botanist_id int IDENTITY(1,1) PRIMARY KEY,
    botanist_name varchar,
    botanist_email varchar UNIQUE
)
GO

CREATE TABLE delta.plant (
    plant_id int PRIMARY KEY,
    species_id int REFERENCES delta.species, 
    country_id int REFERENCES delta.country,
    city_id int REFERENCES delta.city,
    botanist_id int REFERENCES delta.botanist
)
GO

CREATE TABLE delta.reading (
    reading_id int IDENTITY(1,1) PRIMARY KEY,
    plant_id int REFERENCES delta.plant,
    temperature float,
    soil_moisture float,
    last_watered datetime2,
    recording_taken datetime2
)
GO