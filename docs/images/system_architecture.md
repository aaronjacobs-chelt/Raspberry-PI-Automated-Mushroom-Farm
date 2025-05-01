# System Architecture Diagram

This document provides a complete overview of the Raspberry Pi Automated Mushroom Farm system architecture, showing how all components interact to automate humidity control for optimal mushroom cultivation.

## System Diagram

```
                                                                               
                      +-------------------------+                               
                      |                         |                               
 +---------------+    |    Zigbee Network    +--v--+                           
 |               |    |                      |     |                           
 | Zigbee        +<---+--------------------->+     |                           
 | Humidity      |    |                      |     |                           
 | Sensors       |    |                      |     |                           
 +---------------+    |                      |     |                           
                      |                      |     |           RASPBERRY PI    
 +---------------+    |                      |     |  +----------------------+ 
 |               |    |                      |     |  |                      | 
 | Additional    +<---+--------------------->+     |  |  +-----------------+ | 
 | Sensors       |    |                      |     |  |  |                 | | 
 | (Optional)    |    |                      |     +--+->+  Zigbee2MQTT    | | 
 +---------------+    |                      |     |  |  |  Service        | | 
                      |                      |     |  |  |                 | | 
                      |                      |     |  |  +---------+-------+ | 
                      |                      |     |  |            |         | 
 +---------------+    |                      |     |  |            |         | 
 |               |    |                      |     |  |            v         | 
 | Zigbee        +<---+--------------------->+     |  |  +-----------------+ | 
 | Coordinator/  |    |                      |     |  |  |                 | | 
 | Hub           |    |                      |     |  |  |  state.json     | | 
 +---------------+    |                      +-----+  |  |  File           | | 
                      |                         |     |  |                 | | 
                      +-------------------------+     |  +---------+-------+ | 
                                                      |            |         | 
                                                      |            |         | 
                                                      |            v         | 
                                                      |  +-----------------+ | 
                                                      |  |                 | | 
                                                      |  |  Python         | | 
                                                      |  |  Automation     | | 
                                                      |  |  Script         | | 
                                                      |  |                 | | 
                                                      |  +-+-------+------++ | 
                                                      |    |       |      |  | 
                                                      |    |       |      |  | 
                                                      |    v       v      v  | 
                                                      |  +---+ +------+ +--+ | 
                                                      |  |   | |      | |  | | 
                                                      |  |Log| | GPIO | |  | | 
                                                      |  |   | |Ctrl  | |  | | 
                                                      |  +---+ +--+---+ +--+ | 
                                                      |           |          | 
                                                      +-----------|-----------+ 
                                                                  |            
                                                                  v            
                                                       +--------------------+  
                                                       |                    |  
                                                       | Energenie          |  
                                                       | ENER002-2PI        |  
                                                       | Smart Plug         |  
                                                       |                    |  
                                                       +----------+---------+  
                                                                  |            
                                                                  v            
                                                       +--------------------+  
                                                       |                    |  
                                                       | Humidifier         |  
                                                       |                    |  
                                                       +--------------------+  
                                                                               
```

## Data Flow and Communication Protocols

1. **Sensor Data Collection**
   - Zigbee humidity sensors measure environmental conditions (humidity, temperature)
   - Data is transmitted wirelessly using **Zigbee protocol** (IEEE 802.15.4)
   - Typical update frequency: Every 1-5 minutes

2. **Data Processing**
   - Zigbee coordinator receives sensor signals
   - Zigbee2MQTT service translates Zigbee messages to usable data format
   - Data is written to `state.json` file in standardized JSON format
   - Communication: **File I/O**

3. **Automation Decision Logic**
   - Python script (`humidifier_automation.py`) monitors `state.json` file
   - Script reads humidity values and compares to threshold (default: 95%)
   - If humidity is below threshold, humidifier activation is triggered
   - Processing frequency: Configurable, typically every 60 seconds

4. **Control Signal Transmission**
   - GPIO pins are activated in specific sequence
   - Communication protocol: **Direct GPIO digital signals**
   - Signals control the Energenie ENER002-2PI smart plug
   - Power to humidifier is activated/deactivated based on humidity needs

5. **System Monitoring**
   - All activities are logged to `/var/log/humidifier.log`
   - Log entries include timestamps, humidity readings, and actions taken
   - Communication: **File I/O**

## Component Descriptions

### Hardware Components

| Component | Description | Role in System |
|-----------|-------------|----------------|
| **Zigbee Sensors** | Wireless environmental sensors | Monitor humidity and temperature in growing environment |
| **Zigbee Coordinator** | Central hub for Zigbee network | Collects and forwards sensor data to processing software |
| **Raspberry Pi** | Single-board computer | Runs automation software and controls humidifier |
| **Energenie Smart Plug** | GPIO-controlled power outlet | Provides power switching for the humidifier |
| **Humidifier** | Standard home humidifier | Increases humidity when activated |

### Software Components

| Component | Description | Role in System |
|-----------|-------------|----------------|
| **Zigbee2MQTT** | Translation service | Converts Zigbee protocol messages to MQTT and updates state.json |
| **state.json** | Data file | Stores current sensor readings in accessible format |
| **Python Automation Script** | Control logic | Processes sensor data and manages humidifier activation |
| **GPIO Control** | Hardware interface | Provides direct control of Energenie smart plug |
| **Logging System** | Monitoring service | Records all system activities for troubleshooting |

## System Benefits

1. **Reliability**: Multiple sensors ensure accurate readings
2. **Automation**: Maintains optimal conditions without manual intervention
3. **Monitoring**: Comprehensive logging enables performance tracking
4. **Flexibility**: Configurable thresholds and timing to suit different mushroom species
5. **Scalability**: Additional sensors can be added to monitor multiple growing areas

