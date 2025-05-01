# Migration Guide

This guide helps you migrate from the original script-based setup to the new package structure.

## Changes in Version 1.0.0

### Directory Structure

Old structure:
```
/
├── humidifier_automation.py
├── state.json
└── simulate_state_json.py
```

New structure:
```
/
├── src/
│   └── mycomonitor/
│       ├── core/
│       ├── utils/
│       └── interface/
├── tests/
└── examples/
```

### Configuration Changes

1. State File:
   - Old: Direct JSON file
   - New: Managed through configuration

2. GPIO Setup:
   - Old: Hard-coded in script
   - New: Configurable through JSON

3. Logging:
   - Old: Basic file logging
   - New: Configurable handlers

### Code Changes

1. Import Changes:
```python
# Old
import humidifier_automation

# New
from mycomonitor.core import HumidifierController
from mycomonitor.utils import setup_logging
```

2. Configuration:
```python
# Old
HUMIDITY_THRESHOLD = 95.0

# New
from mycomonitor.utils import load_config
config = load_config("/path/to/config.json")
```

3. Controller Usage:
```python
# Old
# Direct script execution

# New
controller = HumidifierController(config)
controller.run()
```

### Data Migration

1. State Data:
   ```bash
   # Backup old state
   cp state.json state.json.backup
   
   # Convert to new format
   python -m mycomonitor.utils.migrate_state
   ```

2. Logs:
   ```bash
   # Archive old logs
   sudo mv /var/log/humidifier.log /var/log/humidifier.log.old
   
   # Set up new logging
   sudo mkdir -p /var/log/mycomonitor
   ```

### System Service

1. Update systemd service:
   ```bash
   sudo systemctl stop humidifier
   sudo mv /etc/systemd/system/humidifier.service /etc/systemd/system/mycomonitor.service
   # Edit service file with new paths
   sudo systemctl daemon-reload
   ```

## Testing Your Migration

1. Verify Configuration:
   ```bash
   python -m mycomonitor.utils.verify_config
   ```

2. Test Run:
   ```bash
   python -m mycomonitor.monitor --dry-run
   ```

3. Check Logs:
   ```bash
   tail -f /var/log/mycomonitor/monitor.log
   ```

## Rollback Procedure

If needed, restore the original setup:

```bash
# Stop new service
sudo systemctl stop mycomonitor

# Restore old files
mv state.json.backup state.json

# Restart old service
sudo systemctl start humidifier
```

## Need Help?

- Open an issue on GitHub
- Check the troubleshooting guide
- Contact support: git@happycaps.co.uk
