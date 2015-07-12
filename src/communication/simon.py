# Main SuperSimon game
from serial import Serial
from threading import Thread
from utils import *
from player import Player
from time import sleep
import struct

# TODO: Need to add byte dumping (last byte > 150ms? Dump buffer)
class SuperSimon:
    def __init__(self, configuration):
        self.__conf = configuration
        self.__initPort()
        self.__operating = False
        self.__readDumpTimeout = 150 # ms
        self.players = []

    def __initPort(self):
        self.__port = Serial(self.__conf.device, baudrate=9600)

    def checkJoins(self):
        joiningThread = Thread(target=self.__protocolJoinState)
        joiningThread.daemon = True
        joiningThread.start()

    def discoverClients(self):
        discoverThread = Thread(target=self.__protocolDiscover)
        discoverThread.daemon = True
        discoverThread.start()

    def checkGameInfo(self, address):
        gameCheckThread = Thread(target=self.__protocolGameInfoRequest, args=[address])
        gameCheckThread.daemon = True
        gameCheckThread.start()

    def sendSequence(self, address, sequence):
        sendSequenceThread = Thread(target=self.__protocolSendSequence, args=[address, sequence])
        sendSequenceThread.daemon = True
        sendSequenceThread.start()

    def startGame(self):
        startGameThread = Thread(target=self.__protocolStartGame)
        startGameThread.daemon = True
        startGameThread.start()

    def exit(self):
        self.__port.close()

    def __findOrCreatePlayer(self, address):
        for player in self.players:
            if player.address == address:
                return player
        player = Player(address)
        self.players.append(player)
        return player

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL HELPERS / THREAD TARGETS
    # ==========================================================================

    def __protocolRequestTurn(self):
        while(self.__operating): continue
        self.__operating = True
        self.__port.flush()

    def __protocolEndTurn(self):
        sleep(0.01) # Sleep for 10ms to allow things to calm down
        self.__operating = False

    def __protocolDiscover(self):
        self.__protocolRequestTurn()
        maximumDiscover = 255
        if self.__conf.discoverMaximum > -1:
            maximumDiscover = min(self.__conf.discoverMaximum, 255)
        for addr in range(0, maximumDiscover):
            discovered = self.__protocolSendDiscover(addr)
            player = self.__findOrCreatePlayer(addr)
            player.online = discovered
            #print("Address " + str(addr) + " discovered = " + str(discovered))
        self.__protocolEndTurn()

    def __protocolJoinState(self):
        self.__protocolRequestTurn()
        for player in self.players:
            if player.online and not player.joined:
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
            # TODO: Share game info
        self.__protocolEndTurn()
        player.checkingGameInfo = False

    def __protocolSendSequence(self, address, sequence):
        self.__protocolRequestTurn()
        player = self.__findOrCreatePlayer(address)
        try:
            self.__protocolSendGameInfo(address, sequence)
        except ValueError as e:
            print(str(e))
            player.online = False
            player.reset()
            print("Address " + str(address) + " has been considered offline")
        self.__protocolEndTurn()

    def __protocolStartGame(self):
        self.__protocolRequestTurn()
        self.__protocolSendStartGame()
        self.__protocolEndTurn()

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL IMPLEMENTATIONS
    # ==========================================================================

    def __protocolRead(self, throwEx = False):
        startTime = millis()
        v = self.__port.read()
        endTime = millis()
        # if self.__port.timeout <= 0:
        #     print("Took " + str(endTime - startTime) + "ms to read byte: '" + str(v) + "'")
        # else:
        #     print("Read '" + str(v) + "' in " + str(endTime - startTime) + "ms with timeout of " + str(self.__port.timeout * 1000.0) + "ms")
        if v == '':
            if throwEx:
                raise ValueError("Failed to read from serial port")
            return None
        return v

    def __protocolSendMagic(self):
        sequence = '\xDE\xAD\xBE\xEF'
        self.__port.write(sequence)

    def __protocolReadMagic(self):
        sequence = ['\xDE', '\xAD', '\xBE', '\xEF']
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
            raise ValueError("Failed to read acknowledge: Invalid byte received (got " + str(b) + ")")

    def __protocolReadJoinResponse(self):
        self.__protocolReadMagic()
        b = self.__protocolRead()
        if b == '\x07':
            return False
        elif b == '\x08':
            return True
        else:
            raise ValueError("Failed to read join response: Invalid byte received (got " + str(b) + ")")

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
            raise ValueError("Failed to read game information response: Invalid byte received (got " + str(b) + ")")

    def __protocolSendDiscover(self, address):
        self.__protocolSendMagic()
        self.__port.write('\x09')
        self.__port.write(chr(address))
        previousTimeout = self.__port.timeout
        self.__port.timeout = 150 / 1000.0 # 150ms timeout
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
        self.__port.timeout = 50 / 1000.0 # 50ms timeout
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
        self.__port.timeout = 150 / 1000.0 # 150ms timeout
        # ValueError is caught by calling code
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
        self.__port.timeout = 50 / 1000.0 # 50ms timeout
        err = None
        try:
            self.__protocolReadAck()
        except ValueError as e:
            err = e
        self.__port.timeout = previousTimeout
        if err is not None:
            raise err

    def __protocolSendStartGame(self):
        self.__protocolSendMagic()
        self.__port.write('\x02')

class PressedButton:
    def __init__(self, button, time):
        self.button = button
        self.time = time
