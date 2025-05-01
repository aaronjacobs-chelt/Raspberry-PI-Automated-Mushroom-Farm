# 🛠️ Development Guide

This guide is intended for developers who want to contribute to or modify the Raspberry Pi Automated Mushroom Farm project.

## 🚀 Getting Started with Development

### Prerequisites

- Python 3.6 or higher
- Git
- Basic understanding of Raspberry Pi GPIO
- Knowledge of Zigbee communication (for sensor-related development)

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm.git
   cd Raspberry-PI-Automated-Mushroom-Farm
   ```

2. Set up a Python virtual environment:
   ```bash
   python3 -m venv ./venv
   source ./venv/bin/activate
   ```

3. Install development dependencies:
   ```bash
   pip install RPi.GPIO pytest
   ```

## 🧪 Testing

### Running Tests

The project uses pytest for testing. To run the tests:

```bash
source ./venv/bin/activate
pytest
```

### Writing Tests

When contributing new features, please include appropriate tests:

1. Place test files in the `tests/` directory
2. Use the naming convention `test_*.py` for test files
3. Ensure tests can run without hardware when possible (use mocks for GPIO)

## 📐 Code Style

This project follows PEP 8 style guidelines. Some key points:

- Use 4 spaces for indentation
- Keep lines to a maximum of 88 characters
- Use meaningful variable and function names
- Include docstrings for all functions and classes

## 📊 Project Structure

```
Raspberry-PI-Automated-Mushroom-Farm/
├── humidifier_automation.py   # Main script for humidity control
├── simulate_state_json.py     # Simulation script for testing
├── state.json                 # Runtime state data
├── docs/                      # Documentation
│   ├── Configuration_Guide.md # Configuration documentation
│   ├── Troubleshooting.md     # Troubleshooting guide
│   └── Development.md         # This development guide
├── tests/                     # Test files
├── venv/                      # Virtual environment (not in version control)
└── README.md                  # Project overview
```

## 🔄 Development Workflow

1. **Create a feature branch** from the main branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them with descriptive messages
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

3. **Run tests** to ensure your changes don't break existing functionality
   ```bash
   pytest
   ```

4. **Push your branch** to GitHub
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** in GitHub against the main branch

## 🔌 Working with GPIO

When developing features that interact with GPIO pins:

- Always clean up GPIO resources when your script exits
- Be aware of pin numbering (this project uses BOARD numbering)
- Test with actual hardware when possible
- Document pin usage clearly

Example of proper GPIO initialization and cleanup:

```python
import RPi.GPIO as GPIO
import atexit

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(22, GPIO.OUT)
    atexit.register(GPIO.cleanup)  # Ensures cleanup on script exit

def control_device(pin, state):
    GPIO.output(pin, state)
```

## 📡 Working with Zigbee

For modifications to Zigbee sensor integration:

- Understand the structure of the `state.json` file
- Test with simulated data using `simulate_state_json.py`
- Be aware of different sensor types and their data formats

## 🤝 Pull Request Guidelines

When submitting a Pull Request:

1. Provide a clear description of the changes
2. Include any necessary documentation updates
3. Ensure all tests pass
4. Reference any related issues using GitHub's issue references
5. Be responsive to code review feedback

## 📚 Resources

- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [Zigbee2MQTT Documentation](https://www.zigbee2mqtt.io/)
- [Python Testing with pytest](https://docs.pytest.org/)

