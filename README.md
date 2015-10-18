# rpi-lock [![Build Status](https://travis-ci.org/chdsbd/rpi-lock.svg)](https://travis-ci.org/chdsbd/rpi-lock)

## What is this?

This is just a project that allows us to open our door with our student ids instead of having to use a key.

In addition to using our RFID cards we can interact with the lock via a web interface, which enables opening of the door as well as managing of logs.

## Web Interface Utilizes

- [Flask](https://github.com/mitsuhiko/flask)
- [Jinja2](http://jinja.pocoo.org)
- [Bootstrap](http://getbootstrap.com)
- [Sortable](https://github.com/HubSpot/sortable)
- [Sqlite](https://sqlite.org)

### Circuit Setup Example

Using [HID MultiCLASS RP40 reader](http://www.hidglobal.com/products/readers/iclass/rp40)

![sketch](/sketch/rpi_lock_bb.png?raw=true)
