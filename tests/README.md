# Tests

This directory contains test files for the Thermostat project.

## Test Structure

```
tests/
├── test_config_reader.py    # Tests for configuration file parsing
├── test_data_send.py         # Tests for Azure IoT Hub data formatting
└── test_utils.py             # Tests for utility functions
```

## Running Tests

Since this is a MicroPython project running on hardware, testing strategies include:

1. **Unit Tests** (Python 3 compatible code)
   - Test configuration parsing logic
   - Test data formatting functions
   - Test timestamp generation

2. **Integration Tests** (on-device)
   - Test sensor reading
   - Test LCD display
   - Test WiFi connectivity

3. **Mock Tests**
   - Mock hardware components for CI/CD testing
   - Mock Azure IoT Hub responses

## Test Framework Options

For MicroPython:
- **unittest** (built-in, limited support on MicroPython)
- **pytest** (requires Python 3 environment with MicroPython stubs)
- Manual test scripts for on-device testing

## Future Work

- [ ] Add unit tests for config_reader.py
- [ ] Add unit tests for data formatting in data_send.py
- [ ] Add integration tests for sensor reading
- [ ] Add mock tests for Azure IoT Hub communication
- [ ] Set up CI/CD pipeline with automated testing
