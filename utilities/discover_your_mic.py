import sounddevice

# Script to discover your mic
devices = sounddevice.query_devices()
print(devices)

default_input_device = sounddevice.default.device[0]
device_info = devices[default_input_device]

print(f"{device_info}")
print(f"Number of input channels: {device_info['max_input_channels']}")