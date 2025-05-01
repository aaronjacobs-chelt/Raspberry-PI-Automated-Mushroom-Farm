# MycoMonitor Usage Guide

## Basic Operation

### Starting the System

1. Initial Setup:
   ```bash
   # Install dependencies
   pip install -e .
   
   # Start the monitor
   sudo python -m mycomonitor.monitor
   ```

2. Configuration:
   - Edit `config.yaml` for custom settings
   - Adjust humidity thresholds
   - Set scheduling preferences

### Monitoring

1. Check Status:
   - View real-time data
   - Check system logs
   - Monitor sensor health

2. Alerts:
   - Configure notification preferences
   - Set alert thresholds
   - Define emergency responses

## Advanced Features

### Custom Scheduling

```python
from mycomonitor.scheduler import Schedule

schedule = Schedule()
schedule.add_humidity_target(
    time="08:00",
    target=85,
    duration="4h"
)
```

### Data Logging

```python
from mycomonitor.logger import DataLogger

logger = DataLogger()
logger.enable_csv_export()
logger.set_interval(minutes=5)
```

### Alert Configuration

```python
from mycomonitor.alerts import AlertManager

alerts = AlertManager()
alerts.add_threshold_alert(
    sensor="main",
    threshold=90,
    condition="above",
    duration="30m"
)
```

## Maintenance

### Regular Tasks

1. Daily:
   - Check sensor readings
   - Verify humidifier operation
   - Monitor logs

2. Weekly:
   - Clean sensors
   - Check connections
   - Backup data
   - Update configurations

3. Monthly:
   - Full system test
   - Calibrate sensors
   - Update software
   - Deep cleaning

### Troubleshooting

1. Common Issues:
   - Connection problems
   - Sensor errors
   - Power interruptions
   - Data inconsistencies

2. Solutions:
   - Check physical connections
   - Restart services
   - Verify configurations
   - Update firmware

## Safety Protocols

1. Emergency Shutdown:
   - Power off procedure
   - Data backup
   - Component protection
   - Recovery steps

2. Environmental Safety:
   - Moisture monitoring
   - Temperature limits
   - Ventilation requirements
   - Chemical safety

