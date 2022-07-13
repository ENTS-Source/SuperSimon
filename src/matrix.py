from socket import *
from threading import Thread
import struct
import requests
import json


discovered_server = None


def find_server():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 8228))
    msg, addr, = s.recvfrom(1024)
    if len(msg) < 4:
        print("Error: length header missing")
        return
    msg_length, = struct.unpack("<L", msg[0:4])
    msg = msg[4:]
    if len(msg) != msg_length:
        print(f"Error: invalid message length. Reported {msg_length} but got {len(msg)}")
        return
    vals = {}
    key = ""
    val = ""
    for c in msg:
        if c == ';':
            if key != "":
                vals[key] = val
                key = ""
            else:
                key = val
            val = ""
        else:
            val += c
    if not vals['A']:
        print("Error: missing 'A' in packet")
        return
    if not vals['P']:
        print("Error: missing 'P' in packet")
        return
    if not vals['S']:
        print("Error: missing 'S' in packet")
        return
    return vals


def send_event(event_type, body):
    thread = Thread(target=send_event_thread, args=(event_type, body,))
    thread.start()


def send_event_thread(event_type, body):
    global discovered_server
    if discovered_server is None:
        print("Locating server...")
        discovered_server = find_server()
        print("Found server: %r" % discovered_server)
    r = requests.put("{}://{}:{}/_matrix/client/r0/rooms/{}/send/{}/{}?access_token={}&user_id={}".format(
        discovered_server['S'], discovered_server['A'], discovered_server['P'],
        discovered_server['ents_rid_ss'], event_type, 'SuperSimon_txn_', discovered_server['ents_as_token'],
        discovered_server['ents_as_prefix']+"supersimon:"+discovered_server['ents_hs_domain'],
    ), json.dumps(body))
    print(f"Matrix request sent. Status: {r.status_code}, content: {r.content}")
