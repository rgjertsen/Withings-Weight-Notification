This blueprint sets up an automation in Home Assistant that send a notification to your phone with the changes in your weight since the last weighing and the changes from the last month.

Weight Change Notification Automation
This automation sends a notification whenever your weight changes, including the change since the last measurement and over the last month.

Requirements
Home Assistant SQL Integration: This automation requires the SQL integration to be set up in your Home Assistant instance.
SQL Sensor: You need to create an SQL sensor that retrieves your weight from one month ago.
Setting Up the SQL Sensor
Install the SQL Integration:

Navigate to Settings > Devices & Services > Integrations.
Click on Add Integration and search for SQL.
Follow the prompts to install the SQL integration.
Configure the SQL Sensor:

Sensor Name: Weight_One_Month_Ago (or any name you prefer).

Database URL: For the default SQLite database, use sqlite:////config/home-assistant_v2.db.

Ensure the number of slashes (////) is correct for SQLite.
SQL Query:

sql
Kopier kode
SELECT s.state
FROM states s
JOIN states_meta sm ON s.metadata_id = sm.metadata_id
WHERE sm.entity_id = 'your_weight_sensor_entity_id'
  AND s.last_updated <= DATETIME('now', '-30 days')
  AND s.state NOT IN ('unknown', 'unavailable', '')
ORDER BY s.last_updated DESC
LIMIT 1
Important: Replace 'your_weight_sensor_entity_id' with the actual entity ID of your weight sensor (e.g., 'sensor.withings_weight').
Column: state

Unit of Measurement: kg

Icon: (Optional) You can set an icon like mdi:weight.

Save the Sensor Configuration:

Complete the setup and ensure the sensor is created.
Verify the SQL Sensor:

Go to Developer Tools > States.
Look for the sensor you just created (e.g., sensor.weight_one_month_ago).
Ensure it has a valid value (not unknown or empty). If it shows unknown, you might not have data from one month ago yet.