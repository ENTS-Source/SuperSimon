# ENTS "Simon Says" game
This is a multiplayer Simon Says game controlled with a Raspberry Pi and Teensys.

For more information, please see [the project page at ents.ca](http://ents.ca/index.php/Super_Simon).

## Information

This is the Raspberry Pi (master game controller) code and game UI. The communication layer is stored as a seperate module for potential implementations in other applications. The game logic may be taken out of this repository in the future for maintainability.

## Running

You'll need a Python 2.7 environment (the default on the Raspberry Pi).

1. Clone the repository
2. `cd` into the `src\` folder
3. Run `pip install -r requirements.txt`
4. Run `python __init__.py` from a graphical environment
