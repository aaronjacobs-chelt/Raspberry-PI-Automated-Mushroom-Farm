# Hardware Setup Guide

## Required Components

1. Raspberry Pi (any model with GPIO)
2. Energenie ENER002-2PI smart plug
3. Zigbee humidity sensors
4. Humidifier unit
5. Zigbee coordinator (for sensor network)

## GPIO Connections

### Energenie ENER002-2PI Pin Mapping

| GPIO Pin (Board) | Function  | Description            |
|-----------------|-----------|------------------------|
| 11              | CTRL1     | Control signal 1       |
| 13              | OUTLET    | Outlet control         |
| 15              | CTRL2     | Control signal 2       |
| 16              | CTRL3     | Control signal 3       |
| 18              | CTRL4     | Control signal 4       |
| 22              | TRIGGER   | Activation trigger     |

### Wiring Instructions

1. Connect Energenie ENER002-2PI to Raspberry Pi:
   - Follow pin mapping table above
   - Ensure solid connections
   - Double-check polarity

2. Safety Considerations:
   - Keep connections away from moisture
   - Use appropriate wire gauge
   - Consider strain relief
   - Use electrical tape or heat shrink

## Sensor Placement

1. Primary Growing Area:
   - Place main sensor at mushroom height
   - Avoid direct water exposure
   - Ensure good air circulation

2. Secondary Sensors:
   - Position at different heights
   - Cover different zones
   - Monitor temperature gradients

## Enclosure Guidelines

1. Raspberry Pi:
   - Use weather-resistant case
   - Ensure ventilation
   - Mount above water level
   - Protect from condensation

2. Power Supply:
   - Use grounded outlet
   - Consider UPS backup
   - Protect from water
   - Use GFCI protection

3. Sensor Protection:
   - Use waterproof enclosures
   - Allow airflow
   - Secure mounting
   - Regular cleaning access

## Network Setup

1. Zigbee Network:
   - Position coordinator centrally
   - Check signal strength
   - Plan for redundancy
   - Document device IDs

## Maintenance Access

1. Component Layout:
   - Allow easy access
   - Label connections
   - Document placement
   - Plan for updates

2. Service Points:
   - Access to reset button
   - Quick disconnect options
   - Spare parts storage
   - Tool requirements

