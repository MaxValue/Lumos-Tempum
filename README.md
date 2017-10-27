# Lumos Tempum
_a daemon to use your smart lights as aid for your circadian rhythm_

## Description
This software controls your smart lights in order to mimic the optimal daylight rhythm for your (human) body.
That means, this does not depend on the sun but on the current time.
You can set your own rhythm by either editing the provided `.csv` file or by pointing to another `.csv` file in the `settings.ini`.

## Notes
**This project is HIGHLY alpha currently, sooo - use at your own risk. (I use it though)**

This project does not support daylight saving time yet, because i think DST was a bad idea altogether.
I do not have to optimal light settings yet, but i will provide them once i know them.

## Requirements
* Smart bulbs. Currently either Zigbee based ones ([Osram Lightify](https://www.osram.com/lightify), [Philips Hue](http://www2.meethue.com/en-us)) or LIFX.
* If you use the Zigbee ones, you need also a Philips Hue hub (for now). I recommend to buy the newer model.
* Some Linux device in your network which runs 24/7 (and can talk to the Philips Hue hub).
* Basic Linux terminal skills (for now). You need to sudo at certain points in the installation.

## How to install
1. Put the folder somewhere on the server you want to run it from. Preferably `/opt/lumostempum/`.
2. If you use a philips hue bridge, first enter the username and the IP address in the config file.
3. Just to make sure everything works, run the script by hand the first time: `./main.py`. You can quit by pressing CTRL + C
4. If it says "Permission denied" you will need to do `chmod +x main.py`.
5. If the directory where you put the files is different from `/opt/lumostempum/`, change all those paths in the `lumostempum@pi.service` file accordingly.
6. Rename the `lumostempum@pi.service` file in order that `pi` is replaced with your username.
7. Copy the `lumostempum@pi.service` file to `/etc/systemd/system/lumostempum@pi.service`. Replace `pi` with your username if it is different and specify the full path to the service file as shown.
8. Do `sudo systemctl --system daemon-reload`.
9. Do `sudo systemctl enable /opt/lumostempum/lumos-tempum@pi`. Replace `pi` with your username if it is different and specify the full path to the service file as shown.
10. Just this one time also do `systemctl start lumos-tempum@pi`. Again, replace `pi` with the correct username.
11. Your lights should adjust by now.

## How you can improve as a smart bulb manufacturer
* Send a refresh event with the complete state of the bulb when the bulb gets (physical) power. Meaning: Do not force consumers to use smart light switches.
* Have a higher maximum brightness (at least 1100 lumen, better 3000 lumen), setting really low brightness levels.
* Have a broader color temperature range (at least 2000-7000 Kelvin)

## How you can improve as a smart hub manufacturer
* Support triggers for physically turning on a light
* Support sending callbacks to clients in the (local) network
* Support setting the color of the light, even when its unreachable and/or off. (The hub should store the state and set it immediately when the light gets reachable)
* Support triggers for groups of lights if any of the lights get reachable. (Or more simply support triggers for any Attribute of a lights state object.)
* You can save yourself all these implementations by just having a circadian rhythm feature. But do it **pro-per-ly**.

Consumers increasingly want this as they get increasingly aware of the importance. Go on. Make some money. Implement this. I believe in you.

## Links
[LIFX blog entry about setting a circadian rhythm](https://www.lifx.com/blogs/light-matters/19034143-the-lighter-side-of-circadian-rhythms) They have this feature now implemented, though.

[A simple project related to this cause](https://www.instructables.com/id/Hueberry/?ALLSTEPS)

[The dlux research project](http://dlux.cae.drexel.edu/)

## Roadmap
* pipe errors to status messages (needs testing)
    > just print
    * function is passed as callback argument
    * plugin calls main function
* web interface to pause daemon (also ALL ON/ALL OFF button)
* WiFi Hotspot instructions for raspberry pi
* remember lights and use that to set values less often
* remember lights and use that to connect to them faster
    * "session.json" in user config directory
    * gets remade at every restart
    * remembers IPs/MAC-Addresses/IDs
* automatic install procedure
* adapter for zigbee
* automatically turn on lights at specified time (in the morning). This will be determined by the curve of the light schedule. If the brightness rises, the light will turn on.
* device profiles about capabilities to calibrate color profile of light automatically
* automatically detect if someone is also issuing commands and pause if so
* custom color profile per light to adjust for light location/setup
* LIFX
    * have permanent socket/server listening for dhcp and udp events
    * act on dhcp events from light bulbs to immediately set color
    * fake the lamps to the LAN to allow being controlled by the default app
* PHILIPS HUE
    * if IP not present, automatically find correct Hue IP
        * through philips site
        * through commonly known urls
            PhilipsHue.home
            PhilipsHue.lan
        * through nmap
        * IMPORTANT: always check if it is hue via the XML file
        * also remember this IP address
    * add username if none is present
* HARDWARE
    * screen to display circadian rhythm
    * rotary to adjust circadian rhythm position
    * hardware casing to elegantly adjust rhythm and display the real rhythm faintly (rotary glass plate with painted hands, behind an e-ink screen which display hands, glass plate has ridged border which turns a wheel which turns rotary)
    * GPIO interface to pause daemon
    * hardware casing for GPIO interface
* APIs
    * fake philips hue API
    * fake LIFX API
        * expose every light as subnet from the hub. Every other device thinks that those are distinct devices as a result.
    * enable local LAN url callbacks for light events
    * add event for reachable flag
    * always remember last state of devices
    * integrate circadian configuration options into API
* Traveldrift: Define when you are soonest in another location and the system gradually shifts the sunrise/sunset times to the target.

## History
I first read about the circadian rhythm in a book by german author Peter Spork called "Wake up!: Aufbruch in eine ausgeschlafene Gesellschaft".
Through this i got aware of light temperatures and their effects on individuals.
I got the idea to use smart bulbs to simulate a natural daylight cycle.
The best systems back then were Philips Hue, because of the adoption by app programmers, but also Osram Lightify, because their bulbs were cheaper and work with the Philips Hue system.
I bought both hubs and an Osram Lightify Bulb.
The Osram hub was needed to update the bulbs firmware to be able to work with the Hue hub.
Teach-In to Osram hub, update firmware, teach-out, teach-in to Philips hub.
I realized that the Philips hub is incapable of setting a default color when the light is physically turned on.
Also it is not possible to trigger an event in the Hue system when a lamp is physically turned on.
I really didn't want to rewire my home just to have smart switches which, of course, are supported by the Hue system to trigger events.
Also, the Hue system is incapable of having a continous curve of color over the day to be applied to the lamps every, say, at least 2 minutes.
At first i wanted to hack the Philips Hue hub to support these features, but they made it quite difficult to alter anything in their software (a single C++ executable doing everything, storing states in a custom format).
While searching for suitable software i came across other projects which helped me developing this.
In the beginning i thought too big and immediately wanted to replace the Hue bridge. That was too complicated, also i didn't know what formula for the lights to use.
I found [this research project](http://dlux.cae.drexel.edu/) which looks kinda dead but it gave me hope that the whole thing is possible ([see their youtube channel](https://www.youtube.com/channel/UCsOSV4Br6XvsntST2aNTAkA))
Then i found [this repository](https://github.com/ancillarymagnet/lifx_circ). He got the drift but it was way to complicated and only supported one manufacturer.
I still don't know if the rhythm described in that repository is as natural as the dlux lab researched (because i could not get a hold of their research results yet).
For replacing the Hue bridge in terms of API, i will use [this repository](https://github.com/jarvisinc/PhilipsHueRemoteAPI)
So for now i will focus on supporting this for Raspberry Pis, but you can run it on any other Linux machine as well.
In the future i will provide 3D-printing instructions to build a case with a knob on it to adjust the light settings.

The overall plan is to make controlling your lights as user-friendly as possible and still support the existing APIs.
