# rpi_lock
Expands upon [simple_wiegand](http://github.com/chdsbd/simple_wiegand) script to do the follow:
- control servo through Raspberry Pi GPIO pins to unlock/lock door
- check binary card data with sqlite database and unlock if the user is authorized


### TO DO:
- [x] Finish doorknob clamp model
- [x] Make clamp from foam board and test **(success)**
- [x] Make clamp out of plywood and test **(worked)**
    - Plywood worked on its own okay
    - Added pieces of drawer liner to provide better connection between wood and metal - rock solid after that
- [x] ~~Make clamp from Lexan (polycarbonate) if plywood fails~~ (Wood didn't fail)
    - Lexan seems more resilient to cracking from bending than plywood
    - Seemed to grip well without needing a cushion layer
    - A little dab of glue might be useful to maintain connection to door knob or a command hook adhesive
    - Thinner than plywood (Lexan 0.093in vs plywood .25)
- [x] Test completed doorknob turning mechanism with servo **(worked)**
    - Polycarbonate gripped doorknob well while the servo turned it
    - Issue: Attaching servo to door with velcro/blue tape will not hold for long (blue tape peals back)
    - Issue: Servo arm attaches at angle to polycarbonate clamp that causes twisting and pulls back velcro
- [x] Make permanent mount for servo from plywood/polycarbonate/acrylic/foamed pvc
    - Made mount from layers of plywood. Laser cutting polycarbonate would have been preferred.
- [x] Test servo mount with whole system
    - Mounted servo on door using refill 3M Command strips. The strips make a super strong connection and are not remotely a weak point.
    - After running a servo test script continuously for a few minutes I noticed some jitter in the servo. It doesn't cause issues with the lock, but it is something that needs to be looked at. I attribute this issue to the RPIO module.
    - servo horn needs to be screwed into servo. It fell off while testing.
    - needed to connect servo horn with screw. Servo arm would fall off without it.
- [x] Create plywood servo arm and attach servo horn to servo via screw
    - Attached servo horn with screw
    - Plywood snapped and original arm works fine with added reinforcement and hole for servo screw to fit through.
- [ ] Add tests for python
- [ ] Add proper logging and change how adding cards work
- [ ] Simplify interface for potential web control


### Potential Expansions
- Door state sensor (open/close)
- Ability to update list remotely
- Status LED
- Create and [print](https://oshpark.com/pricing) circuit board for all connections

### Notes:

Tested using Raspberry Pi B+ with [HID MultiCLASS RP40 reader](http://www.hidglobal.com/products/readers/iclass/rp40)

**CAUTION**: RFID readers typically output data at **5 volts**, you need to lower this to around **3.3 volts** for the Pi (see [voltage divider](https://en.wikipedia.org/wiki/Voltage_divider))

### Setup Example:

![sketch](/sketch/rpi_lock_bb.png?raw=true)

### References:
- [HID RP40 Reader Install Guide](http://www.hidglobal.com/sites/hidglobal.com/files/resource_files/iclass_c_ins_mu_0.pdf)
- [iDoor](https://web.archive.org/web/20150619213423/http://varenhor.st/2009/07/idoor-iphone-controlled-hydraulic-door/) *(web archive)*
- [Amazon product](http://www.amazon.com/Ableware-Door-Knob-Extender-Package/dp/B000PGRKZW?&tag=rnwap-20) ([Image](https://web.archive.org/web/20150720011155/http://ecx.images-amazon.com/images/I/81m3A8GL0cL._SL1500_.jpg))
- Mount plastic on door using [Command Picture Hanging Strips](http://www.amazon.com/Command-Picture-Hanging-4-Small-8-Medium/dp/B000OF6X48?&tag=rnwap-20)
- [Keyfob-Deadbolt](http://www.instructables.com/id/Keyfob-Deadbolt/?ALLSTEPS) (Interesting use of acrylic)

# rpi_flask_interface [![Build Status](https://travis-ci.org/chdsbd/rpi_flask_interface.svg)](https://travis-ci.org/chdsbd/rpi_flask_interface)
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
- [ ] Use same table as rpi_lock
- [ ] Add error [logging](http://flask.pocoo.org/docs/0.10/errorhandling/#application-errors)
- [ ] Send email on bad card read
- [x] Button to unlock door
- [x] Rpi status
- [x] wiegand read_process status
- [x] Customize flash() to show red for errors
- [x] Add tests
- [x] Add Travis-ci
- [ ] Make the deletion of users not cause an entire page reload
- [ ] Make the addition of a user not cause an entire page reload
