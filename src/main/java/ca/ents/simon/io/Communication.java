package ca.ents.simon.io;

import ca.ents.simon.io.device.IODevice;
import ca.ents.simon.io.session.SimonSession;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

/**
 * Central communication platform for communication between players
 */
public class Communication { // TODO: Better name?

    private static ConcurrentMap<IODevice, Communication> DEVICE_MAP = new ConcurrentHashMap<>();

    private IODevice device;
    private Map<Byte, SimonSession> sessions = new HashMap<>();

    public Communication(IODevice device) {
        if (device == null) throw new IllegalArgumentException("IO Device cannot be null");
        this.device = device;
        DEVICE_MAP.put(device, this);
    }

    /**
     * Creates or finds a SimonSession for the given address
     *
     * @param address the address to find or create a session for
     * @return the session for the address
     */
    public SimonSession createOrFindSession(byte address) {
        if (!sessions.containsKey(address))
            sessions.put(address, new SimonSession(address, device.getChannel()));
        return sessions.get(address);
    }

    public static Communication forDevice(IODevice device){
        return DEVICE_MAP.get(device);
    }

}
