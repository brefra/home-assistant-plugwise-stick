"""Support for Plugwise binary sensors."""
import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers import config_validation as cv, entity_platform

from . import PlugwiseNodeEntity
from .const import (
    ATTR_SCAN_DAYLIGHT_MODE,
    ATTR_SCAN_SENSITIVITY_MODE,
    ATTR_SCAN_RESET_TIMER,
    ATTR_SED_STAY_ACTIVE,
    ATTR_SED_SLEEP_FOR,
    ATTR_SED_MAINTENANCE_INTERVAL,
    ATTR_SED_CLOCK_SYNC,
    ATTR_SED_CLOCK_INTERVAL,
    AVAILABLE_SENSOR_ID,
    CB_NEW_NODE,
    DOMAIN,
    MOTION_SENSOR_ID,
    SCAN_SENSITIVITY_MODES,
    SENSORS,
    SERVICE_CONFIGURE_BATTERY,
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
                    platform.async_register_entity_service(
                        SERVICE_CONFIGURE_BATTERY,
                        {
                            vol.Required(ATTR_SED_STAY_ACTIVE): vol.All(
                                vol.Coerce(int), vol.Range(min=1, max=120)
                            ),
                            vol.Required(ATTR_SED_SLEEP_FOR): vol.All(
                                vol.Coerce(int), vol.Range(min=10, max=60)
                            ),
                            vol.Required(ATTR_SED_MAINTENANCE_INTERVAL): vol.All(
                                vol.Coerce(int), vol.Range(min=5, max=1440)
                            ),
                            vol.Required(ATTR_SED_CLOCK_SYNC): cv.boolean,
                            vol.Required(ATTR_SED_CLOCK_INTERVAL): vol.All(
                                vol.Coerce(int), vol.Range(min=60, max=10080)
                            ),
                        },
                        "_service_configure_battery_savings",
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
        sensitivity_mode = kwargs.get(ATTR_SCAN_SENSITIVITY_MODE)
        reset_timer = kwargs.get(ATTR_SCAN_RESET_TIMER)
        daylight_mode = kwargs.get(ATTR_SCAN_DAYLIGHT_MODE)
        _LOGGER.debug(
            "Configure Scan device '%s': sensitivity='%s', reset timer='%s', daylight mode='%s'",
            self.name,
            sensitivity_mode,
            str(reset_timer),
            str(daylight_mode),
        )
        self._node.Configure_scan(reset_timer, sensitivity_mode, daylight_mode)

    def _service_configure_battery_savings(self, **kwargs):
        """Configure battery powered (sed) device service call."""
        stay_active = kwargs.get(ATTR_SED_STAY_ACTIVE)
        sleep_for = kwargs.get(ATTR_SED_SLEEP_FOR)
        maintenance_interval = kwargs.get(ATTR_SED_MAINTENANCE_INTERVAL)
        clock_sync = kwargs.get(ATTR_SED_CLOCK_SYNC)
        clock_interval = kwargs.get(ATTR_SED_CLOCK_INTERVAL)
        _LOGGER.debug(
            "Configure SED device '%s': stay active='%s', sleep for='%s', maintenance interval='%s', clock sync='%s', clock interval='%s'",
            self.name,
            str(stay_active),
            str(sleep_for),
            str(maintenance_interval),
            str(clock_sync),
            str(clock_interval),
        )
        self._node.Configure_SED(
            stay_active,
            maintenance_interval,
            sleep_for,
            clock_sync,
            clock_interval,
        )
