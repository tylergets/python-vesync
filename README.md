# Vesync API in Python
Adds functions to interface with the Vesync API for Etekcity Smart Wifi Outlets.

This library allows you to get a list of devices and turn them on or off

## Usage
```python
import vesync.api
api = vesync.api("USERNAME","PASSWORD")
print(api.get_devices())
api.turn_on("DEVICE_ID")
api.turn_off("DEVICE_ID")
```

## Contributions
Pull requests are welcome. 

## Disclaimer
Not affiliated with the Etekcity Corporation.
