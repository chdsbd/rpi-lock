# rpi-lock [![Build Status](https://travis-ci.org/chdsbd/rpi-lock.svg)](https://travis-ci.org/chdsbd/rpi-lock)

## What is this?

This is just a project that allows us to open our door with our student ids instead of having to use a key.

In addition to using our RFID cards we can interact with the lock via a web interface, which enables opening of the door as well as managing of logs.

## Setup

```bash
git clone https://github.com/chdsbd/rpi-lock &&
bash rpi-lock/install.sh
```

*Note:* The environment variable `RPI_LOCK_CONFIG_PATH` must be set to override the default config values

## Web Interface Utilizes

- [Flask](https://github.com/mitsuhiko/flask)
- [Jinja2](http://jinja.pocoo.org)
- [Bootstrap](http://getbootstrap.com)
- [Sortable](https://github.com/HubSpot/sortable)
- [Sqlite](https://sqlite.org)

### Circuit Setup Example

Using [HID MultiCLASS RP40 reader](http://www.hidglobal.com/products/readers/iclass/rp40)

![sketch](/sketch/rpi_lock_bb.png?raw=true)
