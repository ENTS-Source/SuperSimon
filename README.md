# ENTS "Simon Says" game

A two player version of the popular Simon Says game, with a fifth button.

## Pi Zero (2W) setup

1. Install Raspbian per normal
2. Enable SSH and WiFi to make configuration/development easier
3. `sudo apt update`
4. `sudo apt upgrade`
5. `sudo apt install python3-pgzero` (should already be installed)
6. Turn volume up on the Raspberry Pi and output device (speakers/monitor)
7. `git clone https://github.com/ENTS-Source/SuperSimon.git`
8. `cd SuperSimon`
9. `pgzrun simon.py` (to verify it works)
