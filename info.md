[![hacs][hacsbadge]](hacs)

_Component to integrate with the legacy [Plugwise USB-Stick][Plugwise USB-Stick]._

**This integration supports the following legacy Plugwise devices.**

Devices
- Circle+
- Circle
- Stealth

For each device the following entities are created

platform | Description | Unit | Default state
-- | -- | -- | --
Switch | Relay on/off | n/a | Enabled
Sensor | Ping roundtrip | ms | Disabled
Sensor | Power usage | Watt | Enabled
Sensor | Power usage 8 seconds | Watt | Disabled
Sensor | Power consumption current hour | KWh | Enabled
Sensor | Power consumption previous hour | KWh | Enabled
Sensor | Power consumption today | KWh | Enabled
Sensor | Power consumption yesterday | KWh | Enabled
Sensor | Power production current hour | KWh | Disabled
Sensor | Power production previous hour | KWh | Disabled
Sensor | Inbound RSSI | dBm | Disabled
Sensor | Outbound RSSI | dBm | Disabled

{% if not installed %}
## Installation

Install this integration to Home Assistant using [HACS](https://hacs.xyz)

## Configuration

In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Plugwise USB-Stick". Select the "USB Device path" in the configuration wizard.
When the connection to the USB-stick is found it will automatically discovery all devices.
{% endif %}

## Note

Be aware this integration does NOT support the new [Plug](https://www.plugwise.com/en_US/products/plug) which can be identified by having a local button.
