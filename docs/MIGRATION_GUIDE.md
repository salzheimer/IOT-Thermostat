# Migration Guide: Project Restructure

This document explains the changes made to the project structure and how to work with the new organization.

## What Changed

The project has been reorganized from a flat structure to a modular, organized structure following best practices for MicroPython projects.

### Before (Flat Structure)
```
Thermostat/
├── main.py
├── thermostat.py
├── data_send.py
├── wifi_connect.py
├── config_reader.py
├── lcd_api.py
├── pico_i2c_lcd.py
├── blink.py
├── wifi_scan.py
└── config.txt
```

### After (Organized Structure)
```
Thermostat/
├── src/                 # Application code
│   ├── main.py
│   ├── thermostat.py
│   └── data_send.py
├── drivers/             # Hardware drivers
│   ├── lcd_api.py
│   └── pico_i2c_lcd.py
├── utils/               # Utilities
│   ├── config_reader.py
│   └── wifi_connect.py
├── tools/               # Dev tools
│   ├── blink.py
│   └── wifi_scan.py
├── tests/               # Test files
├── docs/                # Documentation
├── config.txt           # Your config (gitignored)
├── config.example.txt   # Template
└── requirements.txt     # Dependencies
```

## Key Changes

### 1. Directory Organization

| Old Location | New Location | Purpose |
|-------------|--------------|---------|
| `main.py` | `src/main.py` | Application entry point |
| `thermostat.py` | `src/thermostat.py` | Core application logic |
| `data_send.py` | `src/data_send.py` | Azure IoT Hub integration |
| `lcd_api.py` | `drivers/lcd_api.py` | LCD driver abstraction |
| `pico_i2c_lcd.py` | `drivers/pico_i2c_lcd.py` | I2C LCD implementation |
| `config_reader.py` | `utils/config_reader.py` | Configuration parser |
| `wifi_connect.py` | `utils/wifi_connect.py` | WiFi utilities |
| `blink.py` | `tools/blink.py` | Testing utility |
| `wifi_scan.py` | `tools/wifi_scan.py` | WiFi scanner |

### 2. Import Changes

All Python files have been updated with proper import paths:

**Before:**
```python
import thermostat
import config_reader
import wifi_connect as wifi
```

**After:**
```python
import sys
sys.path.append('..')
sys.path.append('../utils')

import src.thermostat as thermostat
from utils import config_reader
from utils import wifi_connect as wifi
```

### 3. New Files Added

- **config.example.txt**: Template configuration file without sensitive data
- **requirements.txt**: Project dependencies and MicroPython version info
- **tests/README.md**: Testing documentation and guidelines
- **tests/test_config_reader.py**: Placeholder for unit tests
- **docs/MIGRATION_GUIDE.md**: This file

## Deployment Changes

### Old Deployment
Copy all `.py` files to the Pico root directory.

### New Deployment
Copy entire directory structure to the Pico:
1. Upload `src/` directory
2. Upload `drivers/` directory
3. Upload `utils/` directory
4. Upload your `config.txt` file

### Using Thonny or rshell
```bash
# Using rshell
rshell cp -r src/ /pyboard/
rshell cp -r drivers/ /pyboard/
rshell cp -r utils/ /pyboard/
rshell cp config.txt /pyboard/
```

## Configuration

### Security Improvement
- `config.txt` remains gitignored
- New `config.example.txt` provides a template
- To set up: `cp config.example.txt config.txt` then edit

## Testing

New test structure added:
- `tests/` directory for all test files
- `tests/README.md` with testing strategies
- Placeholder test files to get started

## Benefits of New Structure

1. **Better Organization**: Clear separation between application code, drivers, utilities, and tools
2. **Scalability**: Easier to add new modules without cluttering the root
3. **Professional**: Follows industry best practices
4. **Testing**: Dedicated space for test files
5. **Security**: Template config file prevents accidental credential commits
6. **Documentation**: Organized docs/ directory for guides

## Backward Compatibility

The new structure is **not backward compatible** with the old flat structure. If you have an existing deployment:

1. Remove all old `.py` files from your Pico
2. Deploy the new directory structure
3. Update your `config.txt` if needed

## Running the Application

Entry point is now:
```python
python src/main.py
```

Or set it as `main.py` on your Pico for auto-start on boot.

## Questions?

If you encounter issues with the new structure:
1. Ensure all directories are copied to the Pico
2. Check that `sys.path` modifications are working
3. Verify `config.txt` is in the root directory (not inside a subdirectory)
