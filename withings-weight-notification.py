blueprint:
  name: Weight Change Notification
  description: >
    Sends a notification when your weight changes, including the change since the last measurement and over the last month.

    **Note:** This blueprint requires you to have an SQL sensor that retrieves your weight from one month ago. See the instructions in the blueprint for how to set this up.
  domain: automation
  input:
    weight_sensor:
      name: Weight Sensor
      description: The entity ID of your weight sensor.
      selector:
        entity:
          domain: sensor
    sql_sensor:
      name: SQL Sensor for Weight One Month Ago
      description: The entity ID of the SQL sensor that retrieves your weight from one month ago.
      selector:
        entity:
          domain: sensor
    notification_service:
      name: Notification Service
      description: The service to use for sending the notification.
      selector:
        service:
          domain: notify
  source_url: https://github.com/yourusername/blueprints/weight_change_notification.yaml

trigger:
  - platform: state
    entity_id: !input weight_sensor

action:
  - service: !input notification_service
    data:
      title: Weight Update
      message: >
        {% set current_weight = states(weight_sensor) | float %}
        {% set previous_weight = trigger.from_state.state | float(0) %}
        {% set weight_change = (current_weight - previous_weight) | round(1) %}
        {% set change_word = 'loss' if weight_change < 0 else 'gain' %}
        {% set weight_change_abs = weight_change | abs %}

        {% set month_ago_weight_state = states(sql_sensor) %}
        {% if month_ago_weight_state not in ['unknown', 'unavailable', '0'] %}
          {% set month_ago_weight = month_ago_weight_state | float(0) %}
          {% set month_change = (current_weight - month_ago_weight) | round(1) %}
          {% set month_change_word = 'loss' if month_change < 0 else 'gain' %}
          {% set month_change_abs = month_change | abs %}
          Your new weight is {{ current_weight }} kg. That's a {{ change_word }} of {{ weight_change_abs }} kg since last time and a {{ month_change_word }} of {{ month_change_abs }} kg over the last month.
        {% else %}
          Your new weight is {{ current_weight }} kg. That's a {{ change_word }} of {{ weight_change_abs }} kg since last time. Data from one month ago is not available.
        {% endif %}

mode: single
