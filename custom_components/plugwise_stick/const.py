"""Const for Plugwise USB-stick."""
from homeassistant.components.binary_sensor import DEVICE_CLASS_MOTION
from homeassistant.components.switch import DEVICE_CLASS_OUTLET
from homeassistant.const import (
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_WATT_HOUR,
    POWER_WATT,
    TIME_MILLISECONDS,
)

DOMAIN = "plugwise_stick"
CONF_USB_PATH = "usb_path"
UNDO_UPDATE_LISTENER = "undo_update_listener"

# Callback types
CB_NEW_NODE = "NEW_NODE"

# Sensor IDs
AVAILABLE_SENSOR_ID = "available"
CURRENT_POWER_SENSOR_ID = "power_1s"
TODAY_ENERGY_SENSOR_ID = "power_con_today"
MOTION_SENSOR_ID = "motion"

# Sensor types
SENSORS = {
    AVAILABLE_SENSOR_ID: {
        "class": None,
        "enabled_default": False,
        "icon": "mdi:signal-off",
        "name": "Available",
        "state": "get_available",
        "unit": None,
    },
    "ping": {
        "class": None,
        "enabled_default": False,
        "icon": "mdi:speedometer",
        "name": "Ping roundtrip",
        "state": "get_ping",
        "unit": TIME_MILLISECONDS,
    },
    CURRENT_POWER_SENSOR_ID: {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": True,
        "icon": None,
        "name": "Power usage",
        "state": "get_power_usage",
        "unit": POWER_WATT,
    },
    "power_8s": {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": False,
        "icon": None,
        "name": "Power usage 8 seconds",
        "state": "get_power_usage_8_sec",
        "unit": POWER_WATT,
    },   
    "power_con_cur_hour": {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": True,
        "icon": None,
        "name": "Power consumption current hour",
        "state": "get_power_consumption_current_hour",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    "power_con_prev_hour": {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": True,
        "icon": None,
        "name": "Power consumption previous hour",
        "state": "get_power_consumption_prev_hour",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    TODAY_ENERGY_SENSOR_ID: {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": True,
        "icon": None,
        "name": "Power consumption today",
        "state": "get_power_consumption_today",
        "unit": ENERGY_KILO_WATT_HOUR, 
    },
    "power_con_yesterday": {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": True,
        "icon": None,
        "name": "Power consumption yesterday",
        "state": "get_power_consumption_yesterday",
        "unit": ENERGY_KILO_WATT_HOUR, 
    },
    "power_prod_cur_hour": {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": False,
        "icon": None,
        "name": "Power production current hour",
        "state": "get_power_production_current_hour",
        "unit": ENERGY_KILO_WATT_HOUR, 
    },
    "power_prod_prev_hour": {
        "class": DEVICE_CLASS_POWER,
        "enabled_default": False,
        "icon": None,
        "name": "Power production previous hour",
        "state": "get_power_production_previous_hour",
        "unit": ENERGY_KILO_WATT_HOUR, 
    },
    "RSSI_in": {
        "class": DEVICE_CLASS_SIGNAL_STRENGTH,
        "enabled_default": False,
        "icon": None,
        "name": "Inbound RSSI",
        "state": "get_in_RSSI",
        "unit": "dBm", 
    },
    "RSSI_out": {
        "class": DEVICE_CLASS_SIGNAL_STRENGTH,
        "enabled_default": False,
        "icon": None,
        "name": "Outbound RSSI",
        "state": "get_out_RSSI",
        "unit": "dBm", 
    },
    MOTION_SENSOR_ID: {
        "class": DEVICE_CLASS_MOTION,
        "enabled_default": True,
        "icon": None,
        "name": "Motion",
        "state": "get_motion",
        "unit": None, 
    }
}

# Switch types
SWITCHES = {
    "relay": {
        "class": DEVICE_CLASS_OUTLET,
        "enabled_default": True,
        "icon": None,
        "name": "Relay state",
        "state": "get_relay_state",
        "switch": "set_relay_state",
        "unit": "state",
    }
}

ATTR_BATTERY_SAVING_AWAKE_DURATION = "awake_duration"
ATTR_BATTERY_SAVING_AWAKE_INTERVAL = "awake_interval"
ATTR_BATTERY_SAVING_SLEEP_DURATION = "sleep_duration"

ATTR_SCAN_DAYLIGHT_MODE = "day_light"
ATTR_SCAN_SENSITIVITY_MODE = "sensitivity_mode"
ATTR_SCAN_RESET_TIMER = "reset_timer"

SCAN_SENSITIVITY_HIGH = "high"
SCAN_SENSITIVITY_MEDIUM = "medium"
SCAN_SENSITIVITY_OFF = "off"
SCAN_SENSITIVITY_MODES = [SCAN_SENSITIVITY_HIGH, SCAN_SENSITIVITY_MEDIUM, SCAN_SENSITIVITY_OFF]

SERVICE_CONFIGURE_SCAN = "configure_scan"