Zigbee Light Production on a Linux Desktop
******************************************

You can produce Zigbee lights on a Linux desktop computer. To make
this happen, you'll need to have the following hardware:

* A code scanner to scan the QR code / barcode of the light
* A hub with Zigbee module - you'll need its IP address and bind secret in order to
  connect to it

The program depends on several Python software packages including:

* evdev: for processing barcode scanner with Linux evdev
* aiohttp: for accessing the web server in an event loop

The production process involves the following stages:

* Wait for light: wait for a light joining the network
* Control light: control the joined light and make sure the correct
  light is being processed.
* Confirm light: confirm the light production and submit the results
  to the server so that databases can be updated

Wait for Light
==============

To start the program, you'll need to enter the following command at a
console (use python3.3 or python3.4 for the PYTHON variable):

${PYTHON} -m zigbee_light.production_line.desktop_linux

Once started, the initial state of the production is to wait for a
Zigbee light. Once a light is detected, the program will automatically
talk to the control hub with Zigbee module and let the light join the
network so that it can be controlled. It will also print out something
like below at the console screen:

Device found: {'mac': 0012343244535646422, 'addr': 12334}

The print out actually shows the lights Zigbee IEEE address and
network address.

Control Light
=============

Once the 'Device found' message pops up, you can try to control the
light and see if the device found by the program is indeed the light
you are going to stick the label to.

To control the light, enter 'f' at the console to turn it off, 'n' to
turn it on.

After controlling the light and if it is the one, enter 'c' to confirm
the light and the system will go into the next state. If the light is
not the one, enter 's' and the system will go back to the previous
'wait for light' state.

Confirm Light
=============

In the confirm state, the program will first wait for the barcode. You
should scan the code at this time. If you found anything wrong, you
may also enter 's' and the program will go back to the initial 'wait
for light' state.

Upon successfully reading the code,
the program will then talk to the server and various
print outs will appear in the console showing the status. You will
probably see:

Submitting to <some url> with <some HTTP post data>

when the program opens the URL to the server and:

Result: {'status': 200}

if everything is OK.

Configuration
=============

The production system may be configured if you are using a different
scanner or a different hub. The script which starts the system is
located at:

zigbee_light/production_line/desktop_linux.py

In that Python script, there's a function called start where you can
pss the scanner name, the hub's address and port and its bind secret.

You can find the scanner name when you plug it into your desktop and
enter command 'dmesg' at the console. The hub's address may be found
in the router's DHCP client list.

Note that on the final production line, the scanner name will probably
be pre-configured. The hub's MAC address will also be
pre-configured and its IP address will be located via arp-scan. This
is a not-so-complete solution to automate some parts of a production system.

