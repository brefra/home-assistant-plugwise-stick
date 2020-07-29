# Plugwise USB-stick Home Assistant Integration

 This is a [Home Assistant](https://home-assistant.io) integration (custom component) for **legacy** [Plugwise](https://www.plugwise.com) Circle+ and [Circle](https://www.plugwise.com/en_US/products/circle) plugs linked to a legacy USB-stick.

![alt tag](https://github.com/brefra/home-assistant-plugwise-stick/blob/master/images/stick.jpg?raw=true "Plugwise USB-Stick")
![alt tag](https://github.com/brefra/home-assistant-plugwise-stick/blob/master/images/plug.jpg?raw=true "Plugwise Circle+ / Circle plug")

Currently this integration supports the devices and functions listed below:

| Plugwise node | Relay control | Power monitoring | Comments |
| ----------- | ----------- | ----------- | ----------- |
| Circle+ | Yes | Yes | Working |
| Circle | Yes | Yes | Working |
| Scan | No | No | Not supported yet |
| Sense | No | No | Not supported yet |
| Switch | No | No | Not supported yet |
| Stealth | Yes | Yes | Experimental (not tested) |
| Sting | No | No | Not supported yet |

## Installation

Install this integration to Home Assistant using [HACS](https://hacs.xyz)

## Configuration

Set up this integration using the UI (configuration/Integrations). Search for "Plugwise USB-Stick" and select the "USB Device path" in the configuration wizard.
When the connection to the USB-stick is initialized it will automatically do a discovery of all linked nodes.

## Note

Be aware this integration does NOT support the new [Plug](https://www.plugwise.com/en_US/products/plug) which can be identified by having a local button.
