"""Support for Plugwise binary sensors."""
import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers import config_validation as cv, entity_platform

from . import PlugwiseNodeEntity
from .const import (
    ATTR_BATTERY_SAVING_AWAKE_DURATION,
    ATTR_BATTERY_SAVING_AWAKE_INTERVAL,
    ATTR_BATTERY_SAVING_SLEEP_DURATION,
    ATTR_SCAN_DAYLIGHT_MODE,
    ATTR_SCAN_SENSITIVITY_MODE,
    ATTR_SCAN_RESET_TIMER,
    AVAILABLE_SENSOR_ID,
    CB_NEW_NODE,
    DOMAIN,
    MOTION_SENSOR_ID,
    SCAN_SENSITIVITY_MODES,
    SENSORS,
    SERVICE_CONFIGURE_SCAN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Plugwise binary sensor based on config_entry."""
    stick = hass.data[DOMAIN][entry.entry_id]["stick"]
    platform = entity_platform.current_platform.get()

    async def async_add_sensor(mac):
        """Add plugwise sensor."""
        _LOGGER.debug("Add binary_sensors for %s", mac)

        node = stick.node(mac)
        for sensor_type in node.get_sensors():
            if sensor_type in SENSORS and sensor_type != AVAILABLE_SENSOR_ID:
                async_add_entities([PlugwiseBinarySensor(node, mac, sensor_type)])
                _LOGGER.debug("Added %s as binary_sensors for %s", mac)

                if node.get_node_type() == "Scan" and sensor_type == MOTION_SENSOR_ID:
                    platform.async_register_entity_service(
                        SERVICE_CONFIGURE_SCAN,
                        {
                            vol.Required(ATTR_SCAN_SENSITIVITY_MODE): vol.In(
                                SCAN_SENSITIVITY_MODES
                            ),
                            vol.Required(ATTR_SCAN_RESET_TIMER): vol.All(
                                vol.Coerce(int), vol.Range(min=1, max=240)
                            ),
                            vol.Required(ATTR_SCAN_DAYLIGHT_MODE): cv.boolean,
                        },
                        "_service_configure_scan",
                    )

    for mac in hass.data[DOMAIN][entry.entry_id]["binary_sensor"]:
        hass.async_create_task(async_add_sensor(mac))

    def discoved_binary_sensor(mac):
        """Add newly discovered binary sensor"""
        hass.async_create_task(async_add_sensor(mac))

    # Listen for discovered nodes
    stick.subscribe_stick_callback(discoved_binary_sensor, CB_NEW_NODE)


class PlugwiseBinarySensor(PlugwiseNodeEntity, BinarySensorEntity):
    """Representation of a Plugwise Binary Sensor."""

    def __init__(self, node, mac, sensor_id):
        """Initialize a Node entity."""
        super().__init__(node, mac)
        self.sensor_id = sensor_id
        self.sensor_type = SENSORS[sensor_id]
        self.node_callbacks = (AVAILABLE_SENSOR_ID, sensor_id)

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self.sensor_type["class"]

    @property
    def entity_registry_enabled_default(self):
        """Return the sensor registration state."""
        return self.sensor_type["enabled_default"]

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.sensor_type["icon"]

    @property
    def name(self):
        """Return the display name of this sensor."""
        return f"{self.sensor_type['name']} ({self._mac[-5:]})"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return getattr(self._node, self.sensor_type["state"])()

    @property
    def unique_id(self):
        """Get unique ID."""
        return f"{self._mac}-{self.sensor_id}"

    def _service_configure_scan(self, **kwargs):
        """Service call to configure motion sensor of Scan device."""
        sensitivity_mode = kwargs.get(ATTR_BATTERY_SAVING_AWAKE_DURATION)
        reset_timer = kwargs.get(ATTR_BATTERY_SAVING_AWAKE_INTERVAL)
        daylight_mode = kwargs.get(ATTR_BATTERY_SAVING_SLEEP_DURATION)
        _LOGGER.debug(
            "Configure Scan device (%s): sensitivity='%s', reset timer='%s', daylight mode='%s'",
            self.name,
            sensitivity_mode,
            str(reset_timer),
            str(daylight_mode),
        )
        self._node.Configure_scan(reset_timer, sensitivity_mode, daylight_mode)

    def _service_configure_sed(self, **kwargs):
        """Configure battery powered (sed) device service call."""
        awake_duration = kwargs.get(ATTR_SCAN_SENSITIVITY_MODE)
        awake_interval = kwargs.get(ATTR_SCAN_RESET_TIMER)
        sleep_duration = kwargs.get(ATTR_SCAN_DAYLIGHT_MODE)
        _LOGGER.debug(
            "Configure SED device (%s): awake duration='%s', awake interval='%s', sleep duration='%s'",
            self._name,
            str(awake_duration),
            str(awake_interval),
            str(sleep_duration),
        )
        self._node.Configure_scan(awake_duration, sleep_duration, awake_interval)
