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
- [ ] Test completed doorknob turning mechanism with servo


### Potential Expansions
- Door state sensor (open/close)
- Ability to update list remotely
- Status LED
- Create and [print](https://oshpark.com/pricing) circuit board for all connections

### References:
- [HID RP40 Reader Install Guide](http://www.hidglobal.com/sites/hidglobal.com/files/resource_files/iclass_c_ins_mu_0.pdf)
- [iDoor](https://web.archive.org/web/20150619213423/http://varenhor.st/2009/07/idoor-iphone-controlled-hydraulic-door/) *(web archive)*
- [Amazon product](http://www.amazon.com/Ableware-Door-Knob-Extender-Package/dp/B000PGRKZW?&tag=rnwap-20) ([Image](https://web.archive.org/web/20150720011155/http://ecx.images-amazon.com/images/I/81m3A8GL0cL._SL1500_.jpg))
- Mount plastic on door using [Command Picture Hanging Strips](http://www.amazon.com/Command-Picture-Hanging-4-Small-8-Medium/dp/B000OF6X48?&tag=rnwap-20)
- [Keyfob-Deadbolt](http://www.instructables.com/id/Keyfob-Deadbolt/?ALLSTEPS) (Interesting use of acrylic)
