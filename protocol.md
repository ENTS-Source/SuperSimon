## SuperSimon Protocol
A communication protocol for a "Simon Says" game developed by [ENTS](http://ents.ca). This communication protocol is intended to be used between a Raspberry Pi and Teensy (as a client). A raw version (that is outdated) can be found [here](https://gist.github.com/turt2live/5d5c14111c8e7933a21f) as a text file.

### Definitions

- `Game` - A round where the user must press a sequence of buttons in the specified order
- `Pi` - The communication master. For SuperSimon, this happens to be a Raspberry Pi
- `Client` - The communication slave(s). For SuperSimon, this happens to be a collection of Teensy microcontrollers
- `Command` - A protocol action for a target to complete or respond to
- `Sequence` - An order of commands to demonstrate a state of the system

### Serial Communication

The Raspberry Pi is expecting 9600/8N1 communication. Any connected client should use the same communication setup.

### Basic overview

Each command will start with a 4 byte magic value. This magic value is always sent before the start of a new command. The magic value is as follows:

`0xDE 0xAD 0xBE 0xEF`

Commands from the Pi will start with the above magic value. Responses from clients should use the following magic value:

`0xCA 0xFE 0xBA 0xBE`

#### Timing

The communications rely on timeouts to assume that clients are either not responsive or not compliant. If bytes are sent farther than 150ms apart then the previous data may be scraped. For example, if the Pi sends 3 bytes of data then takes >50ms to send a fourth byte, then the fourth byte is the start of a new sequence (the other 3 bytes are garbage).

#### Command format

A command is formatted as follows for the protocol:

| Command | Address | Length  | Payload   |
| ------- | ------- | ------- | --------- |
| 8 bits  | 8 bits  | 32 bits | <n> bytes |

If a payload is present, the length will always represent the payload length in bytes. If the payload is not present, the length will not be present. For example, if the payload size is 4 bytes, the length will be the decimal number `4`. The length is represented as a big-endian integer.

The Pi should never send more than 250 bytes total for any command, although the client is expected to be able to send the complete range for the length field of a command.

### Command specification

The following commands are supported by the protocol:

| Command                      | Address?    | Payload?    | Direction | Description                |
| ---------------------------- | ----------- | ----------- | --------- | -------------------------- |
| `0000 0000` / `0x00` / `0`   | No          | No          | Any       | Acknowledge                |
| `0000 0001` / `0x01` / `1`   | Yes         | Yes         | To Client | Game board information     |
| `0000 0010` / `0x02` / `2`   | No          | No          | To Client | Start game                 |
| `0000 0011` / `0x03` / `3`   | Yes         | No          | To Client | Request current game state |
| `0000 0100` / `0x04` / `4`   | No          | No          | To Pi     | "Game not yet finished"    |
| `0000 0101` / `0x05` / `5`   | Yes         | Yes         | To Pi     | Game completed             |
| `0000 0110` / `0x06` / `6`   | Yes         | No          | To Client | Request join state         |
| `0000 0111` / `0x07` / `7`   | No          | No          | To Pi     | Not joined                 |
| `0000 1000` / `0x08` / `8`   | No          | No          | To Pi     | Joined                     |
| `0000 1001` / `0x09` / `9`   | Yes         | No          | To Client | Discover                   |
| `0000 1010` / `0x0A` / `10`  | Yes         | No          | To Client | End game now               |
| `0000 1011` / `0x0B` / `11`  | Yes         | No          | To Client | Reset state (reboot)       |
| `1111 0000` / `0xF0` / `240` | Yes         | Yes         | Any       | Echo                       |

#### Payload specifications for commands

Each command that supports a payload may represent the data however it pleases. Because of this, each supporting command has been documented below.

##### Game board information (`0x01`)

Each byte (8 bits) represents a button number that must be requested. The order of the buttons is the order the buttons must be pressed in.

Example payload: `0x01 0x02 0x01` for  the button sequence `1 - 2 - 1`.

##### Game results (`0x05`)

The payload format is 1 byte for the button number, then 2 bytes for the time (in milliseconds, big-endian) that the user took to press the button. Below is an example of the payload that would be found (times are not to realistic expectations).

| Button | Time to press |
| ------ | ------------- |
| 1      | 1454m         |
| 3      | 657ms         |
| 3      | 378ms         |

Raw payload: `0x01 0x05 0xAE 0x03 0x02 0x91 0x03 0x01 0x7A`

Payload explanation (in order):

- `0x01` - Button 1
- `0x05 0xAE` - 1454 milliseconds
- `0x01` - Button 3
- `0x02 0x91` - 657 milliseconds
- `0x01` - Button 3
- `0x01 0x7A` - 378 milliseconds

If the user failed to complete the sequence then `0xFF 0xFF` should be used for the timing information. For example, if the sequence is 5 buttons and the user fails to complete the sequence on button 2, then buttons 3, 4, and 5 should all have time information of `0xFF 0xFF`. **The payload must contain the complete button sequence sent for the original game sequence.**

The address field for this command is not important as it is ignored by all parties. It may be anything, but it is required to be in line with the protocol.

##### Echo (`0xF0`)

The payload for this command is simply data to be echoed back. The first byte of the payload is the desired target address that was sent by the Pi so that the protocol does not collide with another device (or cause the same device to fall into an infinite send loop).

For example, if the raw payload (represented as numbers) was `9 1 7 1`, then the client should respond with `9 1 7 1` again to address `9` using the same command information.

Example:

- Client receives `0xF0 0x00 <length bytes> 0xAA <more data>`
- Client sends `0xF0 0xAA <length bytes> 0xAA <more data>`

### Sequences

The protocol works off of sequences of commands to describe an action or state within the system. The below assumes that at least 2 clients (addressed as `0x00` and `0x01`) are connected to the system.

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

The discover sequence is used by the Raspberry Pi to determine which clients are within the system. The Pi may use this information to reduce load on the system in other sequences. The Pi will never skip any addresses in this sequence. If the client does not respond correctly within 150ms then the Pi assumes it is not online.

Below is an example of the sequence:

1. Pi sends `Discover` (`0x09`) to address `0x00`
2. Pi waits up to the maximum timeout for `Acknowledge` (`0x00`). If the client fails to respond, the Pi will assume the client is not on the system
3. Pi sends `Discover` (`0x09`) to address `0x01`
4. Pi waits up to the maximum timeout for `Acknowledge` (`0x00`). If the client fails to respond, the Pi will assume the client is not on the system
5. Pi repeats steps 1-4 for addresses `0x02` to `0xFF`

#### Pre-game sequence

This sequence occurs before a game has been started. This sequence is used by the Pi to determine who is going to be participating in the game. The Pi may repeat this sequence many times over any duration to continue to find clients. This Pi will not re-request the join state of a client that has already joined. The client must respond to the Pi's request for the join state within 50ms in order for it to be considered.

Below is an example of the sequence:

1. Pi sends `is joined?` (`0x06`) to address `0x00`
2. Pi waits up to the maximum timeout for `Not joined` (`0x08`) or `Joined` (`0x07`). If the client fails to respond, the Pi will assume the client is not on the system
3. Pi sends `is joined?` (`0x06`) to address `0x01`
4. Pi waits up to the maximum timeout for `Not joined` (`0x08`) or `Joined` (`0x07`). If the client fails to respond, the Pi will assume the client is not on the system
5. Pi repeats steps 1-4 for any address not joined

#### Game sequence

This sequence is for when a game is about to start and for starting the game.

Below is an example of the sequence:

1. Pi sends `Game information` (`0x01`) to address `0x00`
2. Pi waits up to the maximum timeout for `Acknowledge` (`0x00`). If the client fails to respond, the Pi will assume the client has left the system and is no longer present
3. Pi sends `Game information` (`0x01`) to address `0x01`
4. Pi waits up to the maximum timeout for `Acknowledge` (`0x00`). If the client fails to respond, the Pi will assume the client has left the system and is no longer present
5. Pi repeats steps 1-4 for addresses `0x02` to `0xFF`
6. Pi sends `Start game` (`0x02`) (no client responds - broadcast start)

If the client receives a `Start game` (`0x02`) command while still in a game, the client may ignore it.

#### In-game sequence

This sequence is for when a game is currently in progress. The Pi will not re-request any information from any completed clients but will request information from clients that have not completed the game.

Below is an example of the sequence:

1. Pi sends `Game result request` (`0x03`) to address `0x00`
2. Pi waits up to the maximum timeout for `Game results` (`0x05`) or `Game not complete` (`0x04`). If the client fails to respond, the Pi will assume the client has left the system
3. Pi sends `Game result request` (`0x03`) to address `0x01`
4. Pi waits up to the maximum timeout for `Game results` (`0x05`) or `Game not complete` (`0x04`). If the client fails to respond, the Pi will assume the client has left the system
5. Pi repeats steps 1-4 for any address that has not sent a `Game result` (`0x05`) response

The Pi may send an "End game now" (`0x0A`) to any address to terminate the game. This can happen at any point during the "in game" sequence. If the client receives an "End game now" (`0x0A`) command then it must respond with an "Acknowledge" (`0x00`).

### Example game sequence

The following is a sample of the potential order for the Pi to complete sequences. Timing information has been omitted to avoid confusion. The Pi may still follow a slightly different model, however this order is an ideal and expected case.

1. Pi starts `discover` sequence
2. Pi starts `pre-game` sequence
3. Pi starts `game` sequence
4. Pi starts `in-game` sequence
5. Pi starts `pre-game` sequence
6. Pi starts `game` sequence
7. Pi starts `in-game` sequence
