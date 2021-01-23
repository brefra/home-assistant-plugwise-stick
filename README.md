# DEPRECATED - Plugwise USB-stick Home Assistant Integration - DEPRECATED

## Deprecate warning

_This specific custom_component is going to be deprecated soon !_
You can continue to use this installation but it will not been maintained/updated.

I've joined the plugwise team to have the legacy plugwise USB-stick be incorporated into the existing native Plugwise integration at Home Assistant. This is currently in development but not available yet.
In the meanwhile you can use the [plugwise-beta](https://github.com/plugwise/plugwise-beta) version of the Plugwise integration instead by adding the repository manually to HACS.

 This is a [Home Assistant](https://home-assistant.io) integration (custom component) for **legacy** [Plugwise](https://www.plugwise.com) Circle+, [Circle](https://www.plugwise.com/en_US/products/circle) and Stealth devices.

![alt tag](https://github.com/brefra/home-assistant-plugwise-stick/blob/master/images/stick.jpg?raw=true "Plugwise USB-Stick")
![alt tag](https://github.com/brefra/home-assistant-plugwise-stick/blob/master/images/plug.jpg?raw=true "Plugwise Circle+ / Circle plug")

_Be aware this integration does NOT support the new [Plug](https://www.plugwise.com/en_US/products/plug) which can be identified by having a local button !_

Currently this integration supports the devices and functions listed below:

| Plugwise node | Relay control | Power monitoring | Comments |
| ----------- | ----------- | ----------- | ----------- |
| Circle+ | Yes | Yes | Working |
| Circle | Yes | Yes | Working |
| Stealth | Yes | Yes | Experimental (not tested) |

For each device the following entities are created

Entity type | Description | Unit | Default state in HA
-- | -- | -- | --
Switch | Relay on/off | n/a | Enabled
Sensor | Ping roundtrip | ms | Disabled
Sensor | Power usage (last second)| Watt | Enabled
Sensor | Power usage last 8 seconds | Watt | Disabled
Sensor | Power consumption current hour | KWh | Enabled
Sensor | Power consumption previous hour | KWh | Enabled
Sensor | Power consumption today | KWh | Enabled
Sensor | Power consumption yesterday | KWh | Enabled
Sensor | Power production current hour | KWh | Disabled
Sensor | Power production previous hour | KWh | Disabled
Sensor | Inbound RSSI | dBm | Disabled
Sensor | Outbound RSSI | dBm | Disabled

## Installation

Install this integration to Home Assistant using [HACS](https://hacs.xyz)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

## Configuration

In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Plugwise USB-Stick". In the configuration wizard select the "USB Device path" that refers to the USB-Stick or select "Enter Manually" to type it manually.
When the connection to the USB-stick is found it will automatically discovery all linked devices.

## Known issues

- This integration does not support adding (linking) or removing devices to/from the Plugwise network (yet). You still need the [Plugwise Source](https://www.plugwise.com/en_US/source) software for that.
