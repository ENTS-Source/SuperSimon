## SuperSimon Protocol
A communication protocol for a "Simon Says" game developed by [ENTS](http://ents.ca). This communication protocol is intended to be used between a Raspberry Pi and Teensy (as a client). A raw version (that may be outdated) can be found [here](https://gist.github.com/turt2live/5d5c14111c8e7933a21f) as a text file.

### Definitions

- `Game` - A round where the user must press a sequence of buttons in the specified order
- `Pi` - The communication master. For SuperSimon, this happens to be a Raspberry Pi
- `Client` - The communication slave(s). For SuperSimon, this happens to be a collection of Teensy microcontrollers
- `Command` - A protocol action for a target to complete or respond to
- `Sequence` - An order of commands to demonstrate a state of the system

### Basic overview

A command is formatted as follows for the protocol:

| Command | Address | Length  | Payload   |
| ------- | ------- | ------- | --------- |
| 8 bits  | 8 bits  | 32 bits | <n> bytes |

If a payload is present, the length will always represent the payload length in bytes. If the payload is not present, the length will not be present. For example, if the payload size is 4 bytes, the length will be the decimal number `4`.

This protocol works off an all-data model where there is no parity, start bits, or stop bits. Each byte is 8 bits long and the protocol is intended to be read 1 byte (8 bits) at a time.

### Command specification

The following commands are supported by the protocol:

| Command     | Has Address | Has Payload | Direction | Description                |
| ----------- | ----------- | ----------- | --------- | -------------------------- |
| `0000 0000` | No          | No          | Any       | Acknowledge                |
| `0000 0001` | Yes         | Yes         | To Client | Game board information     |
| `0000 0010` | No          | No          | To Client | Start game                 |
| `0000 0011` | Yes         | No          | To Client | Request current game state |
| `0000 0100` | No          | No          | To Pi     | "Game not yet finished     |
| `0000 0101` | Yes         | Yes         | To Pi     | Game completed             |
| `0000 0110` | Yes         | No          | To Client | Request join state         |
| `0000 0111` | No          | No          | To Pi     | Not joined                 |
| `0000 1000` | No          | No          | To Pi     | Joined                     |
| `0000 1001` | Yes         | No          | To Client | Discover                   |

#### Payload specifications for commands

Each command that supports a payload may represent the data however it pleases. Because of this, each supporting command has been documented below.

##### Game board information (`0000 0001`)

Each byte (8 bits) represents a button number that must be requested. The order of the buttons is the order the buttons must be pressed in.

Example payload: `0000 0001 0000 0010 0000 0001` for  the button sequence `1 - 2 - 1`.

##### Game results (`0000 0101`)

The payload format is 1 byte for the button number, then 2 bytes for the time (in milliseconds) that the user took to press the button. Below is an example of the payload that would be found (times are not to realistic expectations).

| Button | Time to press |
| ------ | ------------- |
| 1      | 10ms          |
| 2      | 8ms           |
| 1      | 12ms          |

Raw payload: `0000 0001 0000 1010 0000 0010 0000 1000 0000 0001 0000 1100`

Payload explanation (in order):

- `0000 0001` - Button 1
- `0000 1010` - 10 milliseconds
- `0000 0010` - Button 2
- `0000 1000` - 8 milliseconds
- `0000 0001` - Button 1
- `0000 1100` - 12 milliseconds

If the user failed to complete the sequence then `-1` (decimal, 2's compliment) should be used for the timing information for the pi to know. For example, if the sequence is 5 buttons and the user fails to complete the sequence on button 2, then buttons 3, 4, and 5 should all have the time information of `-1`. **The payload must contain the complete button sequence sent for the original game sequence.**

### Sequences

The protocol works off of sequences of commands to describe an action or state within the system. The below assumes that at least 2 clients (addressed as `0000 0000` and `0000 0001`) are connected to the system.

In general, the following rules are applied to all sequences:

- The maximum timeout for a response is 50ms
- The Pi may skip addresses that it does not know about (see the `Discover` sequence for more information)
- The Pi does not own an address
- The clients are responsible for knowing their own address before joining the communication system
- If a client responds out of turn or incorrectly then the client is in breach of the protocol and is therefore ruining the fun for everyone else
- The client can safely assume that any in-progress game can be destroyed upon receiving the `Pre-game` sequence
- The discover sequence can occur at any time
- The Pi has complete control over who communicates when

#### Discover sequence

The discover sequence is used by the Raspberry Pi to determine which clients are within the system. The Pi may use this information to reduce load on the system in other sequences. The Pi will never skip any addresses in this sequence.

Below is an example of the sequence:

1. Pi sends `Discover` (`0000 1001`) to address `0000 0000`
2. Pi waits up to the maximum timeout for `Acknowledge` (`0000 0000`). If the client fails to respond, the Pi will assume the client is not on the system
3. Pi sends `Discover` (`0000 1001`) to address `0000 0001`
4. Pi waits up to the maximum timeout for `Acknowledge` (`0000 0000`). If the client fails to respond, the Pi will assume the client is not on the system
5. Pi repeats steps 1-4 for addresses `0000 0010` to `1111 1111`

#### Pre-game sequence

This sequence occurs before a game has been started. This sequence is used by the Pi to determine who is going to be participating in the game. The Pi may repeat this sequence many times over any duration to continue to find clients. The Pi may also re-request the join state of a client multiple times.

Below is an example of the sequence:

1. Pi sends `is joined?` (`0000 0110`) to address `0000 0000`
2. Pi waits up to the maximum timeout for `Not joined` (`0000 1000`) or `Joined` (`0000 01111`). If the client fails to respond, the Pi will assume the client is not on the system
3. Pi sends `is joined?` (`0000 0110`) to address `0000 0001`
4. Pi waits up to the maximum timeout for `Not joined` (`0000 1000`) or `Joined` (`0000 01111`). If the client fails to respond, the Pi will assume the client is not on the system
5. Pi repeats steps 1-4 for any address for any amount of time

#### Game sequence

This sequence is for when a game is about to start and for starting the game.

Below is an example of the sequence:

1. Pi sends `Game information` (`0000 0001`) to address `0000 0000`
2. Pi waits up to the maximum timeout for `Acknowledge` (`0000 0000`). If the client fails to respond, the Pi will assume the client has left the system and is no longer present
3. Pi sends `Game information` (`0000 0001`) to address `0000 0001`
4. Pi waits up to the maximum timeout for `Acknowledge` (`0000 0000`). If the client fails to respond, the Pi will assume the client has left the system and is no longer present
5. Pi repeats steps 1-4 for addresses `0000 0010` to `1111 1111`
6. Pi sends `Start game` (`0000 0010`) to address `0000 0000` (no client responds)

#### In-game sequence

This sequence is for when a game is currently in progress. The Pi will not re-request any information from any completed clients but will request information from clients that have not completed the game.

Below is an example of the sequence:

1. Pi sends `Game result request` (`0000 0011`) to address `0000 0000`
2. Pi waits up to the maximum timeout for `Game results` (`0000 0101`) or `Game not complete` (`0000 0100`). If the client fails to respond, the Pi will assume the client has left the system
3. Pi sends `Game result request` (`0000 0011`) to address `0000 0001`
4. Pi waits up to the maximum timeout for `Game results` (`0000 0101`) or `Game not complete` (`0000 0100`). If the client fails to respond, the Pi will assume the client has left the system
5. Pi repeats steps 1-4 for any address that has not sent a `Game result` (`0000 0101`) response

### Example game sequence

The following is a sample of the potential order for the Pi to complete sequences. Timing information has been omitted to avoid confusion. The Pi may still follow a slightly different model, however this order is an ideal and expected case.

1. Pi starts `discover` sequence
2. Pi starts `pre-game` sequence
3. Pi starts `game` sequence
4. Pi starts `in-game` sequence
5. Pi starts `pre-game` sequence
6. Pi starts `game` sequence
7. Pi starts `in-game` sequence 