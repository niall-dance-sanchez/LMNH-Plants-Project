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
    botanist_name, varchar
    email varchar UNIQUE
)
GO

CREATE TABLE delta.plant (
    plant_id int PRIMARY KEY,
    species_id int REFERENCES species, 
    country_id int REFERENCES country,
    city_id int REFERENCES city,
    botanist_id int REFERENCES botanist
)
GO

CREATE TABLE delta.reading (
    reading_id int IDENTITY(1,1) PRIMARY KEY,
    plant_id int REFERENCES plant,
    temperature float,
    soil_moisture float,
    last_watered datetime2,
    recording_taken datetime2
)
GO