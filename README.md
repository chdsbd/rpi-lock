A Flask base web interface to administer my [rpi_lock](https://github.com/chdsbd/rpi_lock)

# Utilizes
- [Flask](https://github.com/mitsuhiko/flask)
- [Jinja2](http://jinja.pocoo.org)
- [Bootstrap](http://getbootstrap.com)
- [Sortable](https://github.com/HubSpot/sortable)
- [Sqlite](https://sqlite.org)

# TODO
- [x] Ability to add add most recent read to RFID Card to Database
- [x] Ability to key in data for card access list
- [x] interface for viewing card access log
- [x] Validate form input
- [x] Add ability to delete users
- [x] interface for card access list
- [ ] must interact with remote tables
- [ ] Add error [logging](http://flask.pocoo.org/docs/0.10/errorhandling/#application-errors)
- [ ] Send email on bad card read
- [x] Button to unlock door
- [ ] Rpi status
- [ ] wiegand read_process status
- [x] Customize flash() to show red for errors
- [x] Add tests
- [ ] Add Travis-ci
