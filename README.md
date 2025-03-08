# ENTS "Simon Says" game
This is a multiplayer Simon Says game controlled with a Raspberry Pi and Teensys.

For more information, please see [the project page at ents.ca](http://ents.ca/index.php/Super_Simon).

## Information

This is the Raspberry Pi (master game controller) code and game UI. The communication layer is stored as a seperate module for potential implementations in other applications. The game logic may be taken out of this repository in the future for maintainability.

## KiCad Setup
In order for the libraries, drawing sheets, and 3D models to load correctly on your machine, you need to open the project and add an environment variable named ENTS_SUPERSIMON_GITHUB_PATH and set it's path to root folder of the repo, wherever you cloned it on your machine. The libraries, drawing sheets, and 3D models all use a relative filepath that begins with whatever path you assigned to ENTS_SUPERSIMON_GITHUB_PATH. This ensure portability of the repo.
![image](https://github.com/user-attachments/assets/bddf1569-ce92-48ee-88c2-e22bfb6aaf66)


## Running

You'll need a Python 2.7 environment (the default on the Raspberry Pi).

1. Clone the repository
2. `cd` into the `src\` folder
3. Run `pip install -r requirements.txt`
4. Run `python __init__.py` from a graphical environment
