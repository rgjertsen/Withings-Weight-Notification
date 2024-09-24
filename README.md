Weight Change Notification Automation

This repository contains a Home Assistant automation blueprint that sends a notification whenever your weight changes, including the change since the last measurement and over the last month.

Table of Contents
Overview
Requirements
Installation
1. Set Up the SQL Sensor
2. Import the Blueprint
3. Create the Automation
Configuration
Troubleshooting
Acknowledgments
Overview
This automation helps you keep track of your weight changes by sending you notifications that include:

The change since your last measurement.
The change over the last month.

Note: The above image is an example of how the notification may appear on your device.

Requirements
Home Assistant (latest version recommended)
SQL Integration in Home Assistant
Weight Sensor (e.g., from a smart scale like Withings)
Notification Service (e.g., Mobile App notifications)
Installation
1. Set Up the SQL Sensor
The automation requires an SQL sensor to retrieve your weight from one month ago. Follow these steps to set it up:

a. Install the SQL Integration
Go to Settings > Devices & Services > Integrations.

Click on Add Integration.

Search for SQL and select it.

Enter the database URL:

perl
Kopier kode
sqlite:////config/home-assistant_v2.db
Note: The number of slashes (////) is important for SQLite databases.

b. Create the SQL Sensor
After adding the SQL integration, you'll need to configure the sensor.

Use the following settings:

Name: Weight One Month Ago (or any name you prefer)

Query:

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
Replace 'your_weight_sensor_entity_id' with the actual entity ID of your weight sensor (e.g., 'sensor.withings_weight').

Column: state

Unit of Measurement: kg

Icon: mdi:weight (optional)

c. Verify the SQL Sensor
Go to Developer Tools > States.
Look for the sensor you just created (e.g., sensor.weight_one_month_ago).
Ensure it has a valid value (not unknown or empty). If it shows unknown, you might not have data from one month ago yet.
