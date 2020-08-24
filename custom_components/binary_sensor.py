"""Support for Plugwise binary sensors."""
from . import PlugwiseNodeEntity
from .const import AVAILABLE_SENSOR_ID, CB_NEW_NODE, DOMAIN, SENSORS
from homeassistant.components.binary_sensor import BinarySensorEntity


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Plugwise binary sensor based on config_entry."""
    stick = hass.data[DOMAIN][entry.entry_id]["stick"]

    async def async_add_sensor(mac):
        """Add plugwise sensor."""
        node = stick.node(mac)
        for sensor_type in node.get_sensors():
            if sensor_type in SENSORS and sensor_type != AVAILABLE_SENSOR_ID:
                async_add_entities([PlugwiseBinarySensor(node, mac, sensor_type)])

    for mac in hass.data[DOMAIN][entry.entry_id]["binary_sensor"]:
        hass.async_create_task(async_add_sensor(mac))

    def discoved_sensor(mac):
        """Add newly discovered binary sensor"""
        hass.async_create_task(async_add_sensor(mac))

    # Listen for discovered nodes
    stick.subscribe_stick_callback(discoved_sensor, CB_NEW_NODE)


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
