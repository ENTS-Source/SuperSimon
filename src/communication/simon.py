# Main SuperSimon game
from time import sleep
import struct

from serial import Serial
from utils import *
from player import Player
from enqueuer import EventQueue


# TODO: Need to add byte dumping (last byte > 150ms? Dump buffer)
class SuperSimon:
    def __init__(self, configuration):
        self.__conf = configuration
        self._init_port()
        self.__readDumpTimeout = 250  # ms
        self.__magicTimeout = 250  # ms
        self.players = []
        self.__queue = EventQueue()

    def _init_port(self):
        self.__port = Serial(self.__conf.device, baudrate=9600)

    def check_joins(self):
        self.__queue.enqueue(self.__protocol_join_state)

    def discover_clients(self):
        self.__queue.enqueue(self.__protocol_discover)

    def check_game_info(self, address):
        self.__queue.enqueue(self.__protocol_game_info_request, [address])

    def send_sequence(self, address, sequence):
        self.__queue.enqueue(self.__protocol_send_sequence, [address, sequence])

    def start_game(self, address):
        self.__queue.enqueue(self.__protocol_start_game, [address])

    def exit(self):
        print("Stopping communication...")
        self.__queue.stop()
        self.__port.close()

    def _find_or_create_player(self, address):
        for player in self.players:
            if player.address == address:
                return player
        player = Player(address)
        self.players.append(player)
        return player

    @staticmethod
    def _format_byte(b):
        if b is None:
            return '<None>'
        return b.encode('hex')

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL HELPERS / THREAD TARGETS
    # ==========================================================================

    # noinspection PyMethodMayBeStatic
    def __protocol_request_turn(self):
        return

    def __protocol_end_turn(self):
        self.__port.flush()
        sleep(0.01)  # Sleep for 10ms to allow things to calm down
        return

    def __protocol_discover(self):
        self.__protocol_request_turn()
        maximum_discover = 255
        if self.__conf.discoverMaximum > -1:
            maximum_discover = min(self.__conf.discoverMaximum, 255)
        for addr in range(0, maximum_discover):
            print("Sending discover to address " + str(addr) + "...")
            discovered = self.__protocol_send_discover(addr)
            player = self._find_or_create_player(addr)
            player.online = discovered
            # print("Address " + str(addr) + " discovered = " + str(discovered))
        self.__protocol_end_turn()

    def __protocol_join_state(self):
        self.__protocol_request_turn()
        for player in self.players:
            if player.online and not player.joined:
                print("Sending join state request to address " + str(player.address) + "...")
                joined = self.__protocol_request_join_state(player.address)
                if joined is None:
                    player.online = False
                    player.reset()
                    print("Address " + str(player.address) + " has been considered as offline")
                else:
                    player.joined = joined
                    # print("Address " + str(player.address) + " joined = " + str(joined))
        self.__protocol_end_turn()

    def __protocol_game_info_request(self, address):
        player = self._find_or_create_player(address)
        if player.checkingGameInfo:
            return
        player.checkingGameInfo = True  # Before protocol lockout to avoid duplicate locks
        self.__protocol_request_turn()
        print("Sending game info request to address " + str(address) + "...")
        game_info = None
        try:
            game_info = self.__protocol_request_game_info(address)
        except ValueError as e:
            print(str(e))
            player.online = False
            player.reset()
            print("Address " + str(address) + " has been considered as offline")
        if game_info is not None:
            player.lastGameInfo = game_info
            player.roundCompleted = True
        self.__protocol_end_turn()
        player.checkingGameInfo = False

    def __protocol_send_sequence(self, address, sequence):
        self.__protocol_request_turn()
        print("Sending sequence to address " + str(address) + "...")
        player = self._find_or_create_player(address)
        try:
            self.__protocol_send_game_info(address, sequence)
        except ValueError as e:
            print(str(e))
            player.online = False
            player.reset()
            print("Address " + str(address) + " has been considered offline")
        self.__protocol_end_turn()

    def __protocol_start_game(self, address):
        self.__protocol_request_turn()
        print("Sending start game...")
        self.__protocol_send_start_game(address)
        self.__protocol_end_turn()

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL IMPLEMENTATIONS
    # ==========================================================================

    def __protocol_read(self, throw_ex=False):
        v = self.__port.read()
        if v == '':
            if throw_ex:
                raise ValueError("Failed to read from serial port: Timeout?")
            return None
        return v

    def __protocol_send_magic(self):
        sequence = '\xDE\xAD\xBE\xEF'
        self.__port.write(sequence)

    def __protocol_read_magic(self):
        sequence = ['\xCA', '\xFE', '\xBA', '\xBE']
        curr_index = 0
        last_read = millis()
        while curr_index < len(sequence):
            b = self.__protocol_read()
            if b is None:
                raise ValueError('Could not read magic value: Timeout')
            now = millis()
            if (now - last_read) > self.__readDumpTimeout:
                curr_index = 0
            if b == sequence[curr_index]:
                curr_index += 1

    def __protocol_read_int(self):
        byte_str = ""
        byte_str += self.__protocol_read(True)
        byte_str += self.__protocol_read(True)
        byte_str += self.__protocol_read(True)
        byte_str += self.__protocol_read(True)
        return struct.unpack(">L", byte_str)[0]

    def __protocol_read_short(self):
        byte_str = ""
        byte_str += self.__protocol_read(True)
        byte_str += self.__protocol_read(True)
        return struct.unpack(">H", byte_str)[0]

    def __protocol_write_int(self, i):
        self.__port.write(struct.pack(">I", i))

    def __protocol_read_ack(self):
        self.__protocol_read_magic()
        b = self.__protocol_read()
        if b != '\x00':
            raise ValueError("Failed to read acknowledge: Invalid byte received (got " + self._format_byte(b) + ")")

    def __protocol_read_join_response(self):
        self.__protocol_read_magic()
        b = self.__protocol_read()
        if b == '\x07':
            return False
        elif b == '\x08':
            return True
        else:
            raise ValueError("Failed to read join response: Invalid byte received (got " + self._format_byte(b) + ")")

    def __protocol_read_game_info_request(self):
        self.__protocol_read_magic()
        b = self.__protocol_read()
        if b == '\x04':
            return None  # No game info
        elif b == '\x05':
            # Has game information
            # noinspection PyUnusedLocal
            address = self.__protocol_read(True)  # Ignored address - not important
            length = self.__protocol_read_int()
            i = 0
            game_info = []
            expecting_button = True
            last_button = None
            while i < length:
                if expecting_button:
                    last_button = ord(self.__protocol_read(True))
                    expecting_button = False
                    i += 1  # Button is 1 byte
                else:
                    ms = self.__protocol_read_short()
                    expecting_button = True
                    i += 2  # Shorts are 2 bytes
                    game_info.append(PressedButton(last_button, ms))
            return game_info
        else:
            raise ValueError(
                "Failed to read game information response: Invalid byte received (got " + self._format_byte(b) + ")")

    def __protocol_send_discover(self, address):
        self.__protocol_send_magic()
        self.__port.write('\x09')
        self.__port.write(chr(address))
        prev_timeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        received = True
        try:
            self.__protocol_read_ack()
        except ValueError as e:
            print(str(e))
            received = False
        self.__port.timeout = prev_timeout
        return received

    def __protocol_request_join_state(self, address):
        self.__protocol_send_magic()
        self.__port.write('\x06')
        self.__port.write(chr(address))
        prev_timeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        try:
            joining = self.__protocol_read_join_response()
        except ValueError as e:
            print(str(e))
            joining = None
        self.__port.timeout = prev_timeout
        return joining

    def __protocol_request_game_info(self, address):
        self.__protocol_send_magic()
        self.__port.write('\x03')
        self.__port.write(chr(address))
        prev_timeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        val = None
        err = None
        try:
            val = self.__protocol_read_game_info_request()
        except ValueError as e:
            err = e
        self.__port.timeout = prev_timeout
        if err:
            raise err
        return val

    def __protocol_send_game_info(self, address, sequence):
        self.__protocol_send_magic()
        self.__port.write('\x01')
        self.__port.write(chr(address))
        self.__protocol_write_int(len(sequence))
        for i in sequence:
            self.__port.write(chr(i))
        prev_timeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        err = None
        try:
            self.__protocol_read_ack()
        except ValueError as e:
            err = e
        self.__port.timeout = prev_timeout
        if err is not None:
            raise err

    def __protocol_send_start_game(self, address):
        self.__protocol_send_magic()
        self.__port.write('\x02')
        self.__port.write(chr(address))


class PressedButton:
    def __init__(self, button, time_to_press):
        self.button = button
        self.time = time_to_press
