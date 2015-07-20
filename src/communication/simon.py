# Main SuperSimon game
from serial import Serial
from threading import Thread
from utils import *
from player import Player
from time import sleep
from enqueuer import EventQueue
import struct

# TODO: Need to add byte dumping (last byte > 150ms? Dump buffer)
class SuperSimon:
    def __init__(self, configuration):
        self.__conf = configuration
        self.__initPort()
        self.__readDumpTimeout = 250 # ms
        self.__magicTimeout = 250 # ms
        self.players = []
        self.__queue = EventQueue()

    def __initPort(self):
        self.__port = Serial(self.__conf.device, baudrate=9600)

    def checkJoins(self):
        self.__queue.enqueue(self.__protocolJoinState)

    def discoverClients(self):
        self.__queue.enqueue(self.__protocolDiscover)

    def checkGameInfo(self, address):
        self.__queue.enqueue(self.__protocolGameInfoRequest, [address])

    def sendSequence(self, address, sequence):
        self.__queue.enqueue(self.__protocolSendSequence, [address, sequence])

    def startGame(self, address):
        self.__queue.enqueue(self.__protocolStartGame, [address])

    def exit(self):
        print("Stopping communication...")
        self.__queue.stop()
        self.__port.close()

    def __findOrCreatePlayer(self, address):
        for player in self.players:
            if player.address == address:
                return player
        player = Player(address)
        self.players.append(player)
        return player

    def __formatByte(self, b):
        if b is None:
            return '<None>'
        return b.encode('hex')

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL HELPERS / THREAD TARGETS
    # ==========================================================================

    def __protocolRequestTurn(self):
        #self.__port.flush()
        return

    def __protocolEndTurn(self):
        self.__port.flush()
        sleep(0.01) # Sleep for 10ms to allow things to calm down
        return

    def __protocolDiscover(self):
        self.__protocolRequestTurn()
        maximumDiscover = 255
        if self.__conf.discoverMaximum > -1:
            maximumDiscover = min(self.__conf.discoverMaximum, 255)
        for addr in range(0, maximumDiscover):
            print("Sending discover to address " + str(addr) + "...")
            discovered = self.__protocolSendDiscover(addr)
            player = self.__findOrCreatePlayer(addr)
            player.online = discovered
            #print("Address " + str(addr) + " discovered = " + str(discovered))
        self.__protocolEndTurn()

    def __protocolJoinState(self):
        self.__protocolRequestTurn()
        for player in self.players:
            if player.online and not player.joined:
                print("Sending join state request to address " + str(player.address) + "...")
                joined = self.__protocolRequestJoinState(player.address)
                if joined is None:
                    player.online = False
                    player.reset()
                    print("Address " + str(player.address) + " has been considered as offline")
                else:
                    player.joined = joined
                    #print("Address " + str(player.address) + " joined = " + str(joined))
        self.__protocolEndTurn()

    def __protocolGameInfoRequest(self, address):
        player = self.__findOrCreatePlayer(address)
        if player.checkingGameInfo: return
        player.checkingGameInfo = True # Before protocol lockout to avoid duplicate locks
        self.__protocolRequestTurn()
        print("Sending game info request to address " + str(address) + "...")
        gameInfo = None
        try:
            gameInfo = self.__protocolRequestGameInfo(address)
        except ValueError as e:
            print(str(e))
            player.online = False
            player.reset()
            print("Address " + str(address) + " has been considered as offline")
        if gameInfo is not None:
            player.lastGameInfo = gameInfo
            player.roundCompleted = True
        self.__protocolEndTurn()
        player.checkingGameInfo = False

    def __protocolSendSequence(self, address, sequence):
        self.__protocolRequestTurn()
        print("Sending sequence to address " + str(address) + "...")
        player = self.__findOrCreatePlayer(address)
        try:
            self.__protocolSendGameInfo(address, sequence)
        except ValueError as e:
            print(str(e))
            player.online = False
            player.reset()
            print("Address " + str(address) + " has been considered offline")
        self.__protocolEndTurn()

    def __protocolStartGame(self, address):
        self.__protocolRequestTurn()
        print("Sending start game...")
        self.__protocolSendStartGame(address)
        self.__protocolEndTurn()

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL IMPLEMENTATIONS
    # ==========================================================================

    def __protocolRead(self, throwEx = False):
        startTime = millis()
        v = self.__port.read()
        endTime = millis()
        #if self.__port.timeout <= 0:
        #    print("Took " + str(endTime - startTime) + "ms to read byte: '" + self.__formatByte(v) + "'")
        #else:
        #    print("Read '" + self.__formatByte(v) + "' in " + str(endTime - startTime) + "ms with timeout of " + str(self.__port.timeout * 1000.0) + "ms")
        if v == '':
            if throwEx:
                raise ValueError("Failed to read from serial port: Timeout?")
            return None
        return v

    def __protocolSendMagic(self):
        sequence = '\xDE\xAD\xBE\xEF'
        self.__port.write(sequence)

    def __protocolReadMagic(self):
        sequence = ['\xCA', '\xFE', '\xBA', '\xBE']
        currentIndex = 0
        lastRead = millis()
        while(currentIndex < len(sequence)):
            b = self.__protocolRead()
            if b is None: raise ValueError('Could not read magic value: Timeout')
            now = millis()
            if (now - lastRead) > self.__readDumpTimeout:
                currentIndex = 0
            if b == sequence[currentIndex]:
                currentIndex += 1

    def __protocolReadInt(self):
        bStr = ""
        bStr += self.__protocolRead(True)
        bStr += self.__protocolRead(True)
        bStr += self.__protocolRead(True)
        bStr += self.__protocolRead(True)
        return struct.unpack(">L", bStr)[0]

    def __protocolReadShort(self):
        bStr = ""
        bStr += self.__protocolRead(True)
        bStr += self.__protocolRead(True)
        return struct.unpack(">H", bStr)[0]

    def __protocolWriteInt(self, i):
        self.__port.write(struct.pack(">I", i))

    def __protocolReadAck(self):
        self.__protocolReadMagic()
        b = self.__protocolRead()
        if b != '\x00':
            raise ValueError("Failed to read acknowledge: Invalid byte received (got " + self.__formatByte(b) + ")")

    def __protocolReadJoinResponse(self):
        self.__protocolReadMagic()
        b = self.__protocolRead()
        if b == '\x07':
            return False
        elif b == '\x08':
            return True
        else:
            raise ValueError("Failed to read join response: Invalid byte received (got " + self.__formatByte(b) + ")")

    def __protocolReadGameInfoRequest(self):
        self.__protocolReadMagic()
        b = self.__protocolRead()
        if b == '\x04':
            return None # No game info
        elif b == '\x05':
            # Has game information
            address = self.__protocolRead(True) # Ignored address - not important
            length = self.__protocolReadInt()
            i = 0
            gameInfo = []
            expectingButton = True
            lastButton = None
            while i < length:
                if expectingButton:
                    lastButton = ord(self.__protocolRead(True))
                    expectingButton = False
                    i = i + 1 # Button is 1 byte
                else:
                    ms = self.__protocolReadShort()
                    expectingButton = True
                    i = i + 2 # Shorts are 2 bytes
                    gameInfo.append(PressedButton(lastButton, ms))
            return gameInfo
        else:
            raise ValueError("Failed to read game information response: Invalid byte received (got " + self.__formatByte(b) + ")")

    def __protocolSendDiscover(self, address):
        self.__protocolSendMagic()
        self.__port.write('\x09')
        self.__port.write(chr(address))
        previousTimeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        received = True
        try:
            self.__protocolReadAck()
        except ValueError as e:
            print(str(e))
            received = False
        self.__port.timeout = previousTimeout
        return received

    def __protocolRequestJoinState(self, address):
        self.__protocolSendMagic()
        self.__port.write('\x06')
        self.__port.write(chr(address))
        previousTimeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        joining = None
        try:
            joining = self.__protocolReadJoinResponse()
        except ValueError as e:
            print(str(e))
            joining = None
        self.__port.timeout = previousTimeout
        return joining

    def __protocolRequestGameInfo(self, address):
        self.__protocolSendMagic()
        self.__port.write('\x03')
        self.__port.write(chr(address))
        previousTimeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        val = None
        err = None
        try:
            val = self.__protocolReadGameInfoRequest()
        except ValueError as e:
            err = e
        self.__port.timeout = previousTimeout
        if err: raise err
        return val

    def __protocolSendGameInfo(self, address, sequence):
        self.__protocolSendMagic()
        self.__port.write('\x01')
        self.__port.write(chr(address))
        self.__protocolWriteInt(len(sequence))
        for i in sequence:
            self.__port.write(chr(i))
        previousTimeout = self.__port.timeout
        self.__port.timeout = self.__magicTimeout / 1000.0
        err = None
        try:
            self.__protocolReadAck()
        except ValueError as e:
            err = e
        self.__port.timeout = previousTimeout
        if err is not None:
            raise err

    def __protocolSendStartGame(self, address):
        self.__protocolSendMagic()
        self.__port.write('\x02')
        self.__port.write(chr(address))

class PressedButton:
    def __init__(self, button, time):
        self.button = button
        self.time = time
