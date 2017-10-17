# Lumos Tempum
_a daemon to use your smart lights as aid for your circadian rhythm_

## How to install
1. Put the folder somewhere on the server you want to run it from. Preferably `/opt/lumostempum/`.
2. If you use a philips hue bridge, first enter the username and the IP address in the config file.
3. Just to make sure everything works, run the script by hand the first time: `./main.py`. You can quit by pressing CTRL + C
4. If it says "Permission denied" you will need to do `chmod +x main.py`.
5. If the directory where you put the files is different from `/opt/lumostempum/`, change all those paths in the `lumostempum@pi.service` file accordingly.
6. Rename the `lumostempum@pi.service` file in order that `pi` is replaced with your username.
7. Do `sudo systemctl --system daemon-reload`.
8. Do `sudo systemctl enable /opt/lumostempum/lumos-tempum@pi`. Replace `pi` with your username if it is different and specify the full path to the service file as shown.
9. Just this one time also do `systemctl start lumos-tempum@pi`. Again, replace `pi` with the correct username.
10. Your lights should adjust by now.

## TO DO's
* pipe errors to status messages
    > just print
    * function is passed as callback argument
    * plugin calls main function
* find out why the daemon crashes after 2 hours

## Roadmap
* automatic install procedure
* web interface to pause daemon
* WiFi Hotspot instructions for raspberry pi
* adapter for zigbee
* remember lights and use that to connect to them faster
    * "session.json" in user config directory
    * gets remade at every restart
    * remembers IPs/MAC-Addresses/IDs
* remember lights and use that to set values less often
* automatically turn on lights at specified time (in the morning)
* device profiles about capabilities
* automatically detect if someone is also issuing commands and pause if so
* custom color profile per light to adjust for light location
* LIFX
    * have permanent socket/server listening for dhcp and udp events
    * act on dhcp events from light bulbs
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

## "Making of" of this project
I used several other projects as reference.
I started out with a small infinite loop which should calculate the values and set them on the devices.
Back then i thought to big and immediately wanted to replace the Hue bridge. That was too complicated, also i didn't know what formula to use.
I found this project http://dlux.cae.drexel.edu/ which looks kinda dead but it gave me hope that the whole thing is possible (see their youtube channel: https://www.youtube.com/channel/UCsOSV4Br6XvsntST2aNTAkA)
Then i found this repository: https://github.com/ancillarymagnet/lifx_circ
I still don't know if the rhythm described in that repository is as natural as the dlux lab researched (because i could not get a hold of their research results yet).
For replacing the Hue bridge in terms of API, i used this repository: https://github.com/jarvisinc/PhilipsHueRemoteAPI
