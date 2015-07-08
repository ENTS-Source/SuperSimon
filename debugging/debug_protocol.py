# These methods are intended to be copy/pasted into the IDLE client
# for debugging.

import random
from time import sleep, time
from serial import Serial
import RPi.GPIO as GPIO
import struct

def millis():
    return int(round(time() * 1000))


def intToBytes(i):
    return struct.pack('>I', i)


def readInt():
    lStr = ""
    lStr += port.read()
    lStr += port.read()
    lStr += port.read()
    lStr += port.read()
    return struct.unpack(">L", lStr)[0]


def readShort():
    lStr = ""
    lStr += port.read()
    lStr += port.read()
    return struct.unpack(">H", lStr)[0]


def rts():
    #GPIO.output(11, GPIO.HIGH)
    port.write(chr(222)) # 0xDE
    port.write(chr(173)) # 0xAD
    port.write(chr(190)) # 0xBE
    port.write(chr(239)) # 0xEF
    return


def cts():
    #sleep(0.01) # Just to ensure we don't chop off data
    #GPIO.output(11, GPIO.LOW)
    return

def readMagic():
    port.read()
    port.read()
    port.read()
    port.read()


def sendAck():
    print("Sending ACK...")
    rts()
    port.write(chr(0))
    print("ACK sent!")


def sendGameInfo(addr, sLen):
    print("Sending game sequence...")
    rts()
    port.write(chr(1))
    port.write(chr(addr))
    port.write(intToBytes(sLen))
    for i in range(0, sLen):
        s = random.randint(1, 5)
        print("S[" + str(i) + "] = " + str(s))
        port.write(chr(s))
    cts()
    print("Game sequence sent! Waiting for ACK...")
    start = millis()
    r = port.read()
    end = millis()
    if r != chr(0):
        print("Unexpected response character: " + str(ord(r)))
    else:
        print("Received ACK in " + str(end - start) + "ms")


def startGame():
    print("Sending start game command...")
    rts()
    port.write(chr(2))
    cts()
    # No response
    print("Start game sent!")


def requestGameState(addr):
    print("Sending request for game state...")
    rts()
    port.write(chr(3))
    port.write(chr(addr))
    cts()
    print("Game state request sent! Waiting for response...")
    start = millis()
    r = port.read()
    end = millis()
    print("Got response in " + str(end - start) + "ms")
    if r == chr(4):
        print("Game not yet complete")
    elif r == chr(5):
        print("Game completed, gathering data about game")
        a = port.read() # Ignored byte
        l = readInt()
        print("Address receive = " + str(ord(a)) + ", expecting " + str(l) + " bytes of game data")
        expectingButton = True
        lastButton = None
        i = 0
        while i < l:
            if expectingButton:
                lastButton = ord(port.read())
                expectingButton = False
                i = i + 1
            else:
                ms = readShort()
                expectingButton = True
                i = i + 2 # Cause shorts are 2 bytes
                print("Button " + str(lastButton) + " took " + str(ms) + "ms to press")
        print("Game data read")
    else:
        print("Unknown response: " + str(r))


def isJoining(addr):
    print("Sending join state request...")
    rts()
    port.write(chr(6))
    port.write(chr(addr))
    cts()
    print("Join state request sent! Waiting for response...")
    start = millis()
    r = port.read()
    end = millis()
    print("Got response in " + str(end - start) + "ms")
    if r == chr(7):
        print("Not joined")
    elif r == chr(8):
        print("Joined")
    else:
        print("Unknown response: " + str(ord(r)))


def discover(addr):
    print("Sending discover...")
    rts()
    port.write(chr(9))
    port.write(chr(addr))
    cts()
    print("Discover sent! Waiting for response...")
    start = millis()
    r = port.read()
    end = millis()
    if r == chr(0):
        print("Discovered in " + str(end - start) + "ms")
    else:
        print("Unknown response: " + str(ord(r)))


def echo(addr, raddr, sendBytes = 2):
    print("Sending echo...")
    rts()
    port.write(chr(240))
    port.write(chr(addr))
    port.write(intToBytes(sendBytes))
    port.write(chr(raddr))
    for i in range(0, sendBytes - 1):
        r = random.randint(1, 200)
        c = chr(r)
        port.write(c)
        print("Out = " + str(r))
    cts()
    print("Echo sent! Waiting for response...")
    start = millis()
    readMagic()
    r = port.read()
    end = millis()
    print("Got response in " + str(end - start) + "ms")
    if r == chr(240):
        print("Got echo back, reading data...")
        a = port.read()
        l = readInt()
        print("Expecting " + str(l) + " bytes back")
        d1 = port.read()
        for i in range(0, sendBytes - 1):
            v = port.read()
            print("Read " + str(ord(v)))
        print("Response to address " + str(ord(a)))
        print("  Length = " + str(l))
        print("  D1 = " + str(ord(d1)))
        print("")
    else:
        print("Unknown response: " + str(ord(r)))
