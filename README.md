# Vesync API in Python
Adds functions to interface with the Vesync API for Etekcity Smart Wifi Outlets.

This library allows you to get a list of devices, get a device's usage details and configuration, and turn devices on or off

## Usage
```python
from vesync.api import VesyncApi
api = VesyncApi("USERNAME","PASSWORD")
print(api.get_devices())
api.turn_on("DEVICE_ID")
api.turn_off("DEVICE_ID")
print(api.get_detail("DEVICE_ID"))
print(api.get_config("DEVICE_ID"))
```

## Contributions
Pull requests are welcome.

## Disclaimer
Not affiliated with the Etekcity Corporation.
