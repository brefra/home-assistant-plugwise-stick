"""Support for Plugwise devices connected to a Plugwise USB-stick."""
import asyncio
import logging
import voluptuous as vol

import plugwise
from plugwise.exceptions import (
    CirclePlusError,
    NetworkDown,
    PortError,
    StickInitError,
    TimeoutException,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity

from .const import (
    ATTR_MAC_ADDRESS,
    AVAILABLE_SENSOR_ID,
    CONF_USB_PATH,
    DOMAIN,
    SENSORS,
    SERVICE_DEVICE_ADD,
    SERVICE_DEVICE_FEATURES,
    SERVICE_DEVICE_REMOVE,
    UNDO_UPDATE_LISTENER,
)

_LOGGER = logging.getLogger(__name__)
CB_TYPE_NEW_NODE = "NEW_NODE"
PLUGWISE_STICK_PLATFORMS = ["switch", "sensor", "binary_sensor"]


async def async_setup(hass, config):
    """Set up the Plugwise stick component."""
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Establish connection with plugwise USB-stick."""
    hass.data.setdefault(DOMAIN, {})

    def discover_finished():
        """Create entities for all discovered nodes."""
        nodes = stick.nodes()
        _LOGGER.info(
            "Discovered %s out of %s registered nodes",
            str(len(nodes)),
            str(stick.registered_nodes()),
        )
        for component in PLUGWISE_STICK_PLATFORMS:
            hass.data[DOMAIN][config_entry.entry_id][component] = []
            for mac in nodes:
                if component in stick.node(mac).get_categories():
                    hass.data[DOMAIN][config_entry.entry_id][component].append(mac)
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, component)
            )
        stick.auto_update()
        # Enable reception of join request and automatically accept new node join requests
        stick.allow_join_requests(True, True)

    def shutdown(event):
        hass.async_add_executor_job(stick.disconnect)

    stick = plugwise.stick(config_entry.data[CONF_USB_PATH])
    hass.data[DOMAIN][config_entry.entry_id] = {"stick": stick}
    try:
        _LOGGER.debug("Connect to USB-Stick")
        await hass.async_add_executor_job(stick.connect)
        _LOGGER.debug("Initialize USB-stick")
        await hass.async_add_executor_job(stick.initialize_stick)
        _LOGGER.debug("Discover Circle+ node")
        await hass.async_add_executor_job(stick.initialize_circle_plus)
    except PortError:
        _LOGGER.error("Connecting to Plugwise USBstick communication failed")
        raise ConfigEntryNotReady
    except StickInitError:
        _LOGGER.error("Initializing of Plugwise USBstick communication failed")
        await hass.async_add_executor_job(stick.disconnect)
        raise ConfigEntryNotReady
    except NetworkDown:
        _LOGGER.warning("Plugwise zigbee network down")
        await hass.async_add_executor_job(stick.disconnect)
        raise ConfigEntryNotReady
    except CirclePlusError:
        _LOGGER.warning("Failed to connect to Circle+ node")
        await hass.async_add_executor_job(stick.disconnect)
        raise ConfigEntryNotReady
    except TimeoutException:
        _LOGGER.warning("Timeout")
        await hass.async_add_executor_job(stick.disconnect)
        raise ConfigEntryNotReady
    _LOGGER.debug("Start discovery of registered nodes")
    stick.scan(discover_finished)

    # Listen when EVENT_HOMEASSISTANT_STOP is fired
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, shutdown)

    # Listen for entry updates
    hass.data[DOMAIN][config_entry.entry_id][
        UNDO_UPDATE_LISTENER
    ] = config_entry.add_update_listener(_async_update_listener)

    async def device_add(service):
        """Manually add device to Plugwise zigbee network"""
        stick.node_join(service.data[ATTR_MAC_ADDRESS])

    async def device_remove(service):
        """Manually remove device from Plugwise zigbee network"""
        stick.node_unjoin(service.data[ATTR_MAC_ADDRESS])

    async def device_features(service):
        """Manually remove device from Plugwise zigbee network"""
        stick.node(service.data[ATTR_MAC_ADDRESS])._request_features()

    service_device_schema = vol.Schema({vol.Required(ATTR_MAC_ADDRESS): cv.string})

    hass.services.async_register(
        DOMAIN, SERVICE_DEVICE_ADD, device_add, service_device_schema
    )
    hass.services.async_register(
        DOMAIN, SERVICE_DEVICE_REMOVE, device_remove, service_device_schema
    )
    hass.services.async_register(
        DOMAIN, SERVICE_DEVICE_FEATURES, device_features, service_device_schema
    )

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload the Plugwise stick connection."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(config_entry, component)
                for component in PLUGWISE_STICK_PLATFORMS
            ]
        )
    )
    hass.data[DOMAIN][config_entry.entry_id][UNDO_UPDATE_LISTENER]()
    if unload_ok:
        stick = hass.data[DOMAIN][config_entry.entry_id]["stick"]
        await hass.async_add_executor_job(stick.disconnect)
        hass.data[DOMAIN].pop(config_entry.entry_id)
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, config_entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)


class PlugwiseNodeEntity(Entity):
    """Base class for a Plugwise entities."""

    def __init__(self, node, mac):
        """Initialize a Node entity."""
        self._node = node
        self._mac = mac
        self.node_callbacks = (AVAILABLE_SENSOR_ID,)

    async def async_added_to_hass(self):
        """Subscribe to updates."""
        for node_callback in self.node_callbacks:
            self._node.subscribe_callback(self.sensor_update, node_callback)

    async def async_will_remove_from_hass(self):
        """Unsubscribe to updates."""
        for node_callback in self.node_callbacks:
            self._node.unsubscribe_callback(self.sensor_update, node_callback)

    @property
    def available(self):
        """Return the availability of this entity."""
        return getattr(self._node, SENSORS[AVAILABLE_SENSOR_ID]["state"])()

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._mac)},
            "name": f"{self._node.get_node_type()} ({self._mac})",
            "manufacturer": "Plugwise",
            "model": self._node.get_node_type(),
            "sw_version": f"{self._node.get_firmware_version()}",
        }

    @property
    def name(self):
        """Return the display name of this entity."""
        return f"{self._node.get_node_type()} {self._mac[-5:]}"

    def sensor_update(self, state):
        """Handle status update of Entity."""
        self.schedule_update_ha_state()

    @property
    def should_poll(self):
        """Disable polling."""
        return False

    @property
    def unique_id(self):
        """Get unique ID."""
        return f"{self._mac}-{self._node.get_node_type()}"
