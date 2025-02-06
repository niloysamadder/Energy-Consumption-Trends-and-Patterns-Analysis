-- Create Dimension Tables

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_temperature (
    temperature_id INTEGER AUTOINCREMENT PRIMARY KEY,
    temperature FLOAT UNIQUE
);

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_humidity (
    humidity_id INTEGER AUTOINCREMENT PRIMARY KEY,
    humidity FLOAT UNIQUE
);

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_squarefootage (
    squarefootage_id INTEGER AUTOINCREMENT PRIMARY KEY,
    squarefootage FLOAT UNIQUE
);

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_occupancy (
    occupancy_id INTEGER AUTOINCREMENT PRIMARY KEY,
    occupancy INT UNIQUE
);

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_hvac_usage (
    hvac_id INTEGER AUTOINCREMENT PRIMARY KEY,
    hvac_usage BOOLEAN UNIQUE
);

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_lighting_usage (
    lighting_id INTEGER AUTOINCREMENT PRIMARY KEY,
    lighting_usage BOOLEAN UNIQUE
);

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_renewable_energy (
    renewable_id INTEGER AUTOINCREMENT PRIMARY KEY,
    renewable_energy FLOAT UNIQUE
);

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.dim_holiday (
    holiday_id INTEGER AUTOINCREMENT PRIMARY KEY,
    holiday BOOLEAN UNIQUE
);



-- Create Fact Table

CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.fact_energy_consumption (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    timestamp TIMESTAMP,
    temperature_id INTEGER,
    humidity_id INTEGER,
    squarefootage_id INTEGER,
    occupancy_id INTEGER,
    hvac_id INTEGER,
    lighting_id INTEGER,
    renewable_id INTEGER,
    holiday_id INTEGER,
    hour INTEGER,
    weekend BOOLEAN,
    energy_consumption FLOAT,
    FOREIGN KEY (temperature_id) REFERENCES energy_consumption_db.consumption_schema.dim_temperature(temperature_id),
    FOREIGN KEY (humidity_id) REFERENCES energy_consumption_db.consumption_schema.dim_humidity(humidity_id),
    FOREIGN KEY (squarefootage_id) REFERENCES energy_consumption_db.consumption_schema.dim_squarefootage(squarefootage_id),
    FOREIGN KEY (occupancy_id) REFERENCES energy_consumption_db.consumption_schema.dim_occupancy(occupancy_id),
    FOREIGN KEY (hvac_id) REFERENCES energy_consumption_db.consumption_schema.dim_hvac_usage(hvac_id),
    FOREIGN KEY (lighting_id) REFERENCES energy_consumption_db.consumption_schema.dim_lighting_usage(lighting_id),
    FOREIGN KEY (renewable_id) REFERENCES energy_consumption_db.consumption_schema.dim_renewable_energy(renewable_id),
    FOREIGN KEY (holiday_id) REFERENCES energy_consumption_db.consumption_schema.dim_holiday(holiday_id)
);


-- Load Data into Dimension Tables

INSERT INTO energy_consumption_db.consumption_schema.dim_temperature (temperature)
SELECT DISTINCT temperature FROM energy_consumption_db.consumption_schema.energy_consumption;

INSERT INTO energy_consumption_db.consumption_schema.dim_humidity (humidity)
SELECT DISTINCT humidity FROM energy_consumption_db.consumption_schema.energy_consumption;

INSERT INTO energy_consumption_db.consumption_schema.dim_squarefootage (squarefootage)
SELECT DISTINCT squarefootage FROM energy_consumption_db.consumption_schema.energy_consumption;

INSERT INTO energy_consumption_db.consumption_schema.dim_occupancy (occupancy)
SELECT DISTINCT occupancy FROM energy_consumption_db.consumption_schema.energy_consumption;

INSERT INTO energy_consumption_db.consumption_schema.dim_hvac_usage (hvac_usage)
SELECT DISTINCT hvacusage FROM energy_consumption_db.consumption_schema.energy_consumption;

INSERT INTO energy_consumption_db.consumption_schema.dim_lighting_usage (lighting_usage)
SELECT DISTINCT lightingusage FROM energy_consumption_db.consumption_schema.energy_consumption;

INSERT INTO energy_consumption_db.consumption_schema.dim_renewable_energy (renewable_energy)
SELECT DISTINCT renewableenergy FROM energy_consumption_db.consumption_schema.energy_consumption;

INSERT INTO energy_consumption_db.consumption_schema.dim_holiday (holiday)
SELECT DISTINCT holiday FROM energy_consumption_db.consumption_schema.energy_consumption;


-- Load Data into Fact Table

INSERT INTO energy_consumption_db.consumption_schema.fact_energy_consumption (
    timestamp, temperature_id, humidity_id, squarefootage_id, occupancy_id,
    hvac_id, lighting_id, renewable_id, holiday_id, hour, weekend, energy_consumption
)
SELECT 
    e.timestamp,
    t.temperature_id,
    h.humidity_id,
    s.squarefootage_id,
    o.occupancy_id,
    hv.hvac_id,
    l.lighting_id,
    r.renewable_id,
    ho.holiday_id,
    e.hour,
    e.weekend,
    e.energyconsumption
FROM energy_consumption_db.consumption_schema.energy_consumption e
JOIN energy_consumption_db.consumption_schema.dim_temperature t ON e.temperature = t.temperature
JOIN energy_consumption_db.consumption_schema.dim_humidity h ON e.humidity = h.humidity
JOIN energy_consumption_db.consumption_schema.dim_squarefootage s ON e.squarefootage = s.squarefootage
JOIN energy_consumption_db.consumption_schema.dim_occupancy o ON e.occupancy = o.occupancy
JOIN energy_consumption_db.consumption_schema.dim_hvac_usage hv ON e.hvacusage = hv.hvac_usage
JOIN energy_consumption_db.consumption_schema.dim_lighting_usage l ON e.lightingusage = l.lighting_usage
JOIN energy_consumption_db.consumption_schema.dim_renewable_energy r ON e.renewableenergy = r.renewable_energy
JOIN energy_consumption_db.consumption_schema.dim_holiday ho ON e.holiday = ho.holiday;


