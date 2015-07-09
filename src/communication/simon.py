# Main SuperSimon game
from serial import Serial
from threading import Thread
from utils import *

class SuperSimon:
    def __init__(self, configuration):
        self.__conf = configuration
        self.__initPort()
        self.__operating = False
        self.__readDumpTimeout = 50 # ms

    def __initPort(self):
        self.__port = Serial(self.__conf.device, baudrate=9600)

    def discoverClients(self):
        discoverThread = Thread(target=self.__protocolDiscover)
        discoverThread.daemon = True
        discoverThread.start()

    def exit(self):
        self.__port.close()

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL HELPERS / THREAD TARGETS
    # ==========================================================================

    def __protocolRequestTurn(self):
        while(self.__operating): continue
        self.__operating = True

    def __protocolEndTurn(self):
        self.__operating = False

    def __protocolDiscover(self):
        self.__protocolRequestTurn()
        maximumDiscover = 255
        if self.__conf.discoverMaximum > -1:
            maximumDiscover = min(self.__conf.discoverMaximum, 255)
        for addr in range(0, maximumDiscover):
            discovered = self.__protocolSendDiscover(addr)
            print("Address " + str(addr) + " discovered = " + str(discovered))
        self.__protocolEndTurn()

    # ==========================================================================
    # BELOW HERE ARE THE PROTOCOL IMPLEMENTATIONS
    # ==========================================================================

    def __protocolRead(self):
        startTime = millis()
        v = self.__port.read()
        endTime = millis()
        # if self.__port.timeout <= 0:
        #     print("Took " + str(endTime - startTime) + "ms to read byte: '" + str(v) + "'")
        # else:
        #     print("Read '" + str(v) + "' in " + str(endTime - startTime) + "ms with timeout of " + str(self.__port.timeout * 1000.0) + "ms")
        if v == '':
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

    def __protocolReadAck(self):
        self.__protocolReadMagic()
        b = self.__protocolRead()
        if b != '\x00':
            raise ValueError("Failed to read acknowledge: Invalid byte received (got " + str(b) + ")")

    def __protocolSendDiscover(self, address):
        self.__protocolSendMagic()
        self.__port.write('\x09')
        self.__port.write(chr(address))
        previousTimeout = self.__port.timeout
        self.__port.timeout = 50 / 1000.0 # 50ms timeout
        received = True
        try:
            self.__protocolReadAck()
        except ValueError as e:
            print(str(e))
            # Failed to respond
            received = False
        self.__port.timeout = previousTimeout
        return received
