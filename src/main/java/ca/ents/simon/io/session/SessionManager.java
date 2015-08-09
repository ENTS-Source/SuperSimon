package ca.ents.simon.io.session;

import ca.ents.simon.io.device.IODevice;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

/**
 * Session manager for dealing with SimonSessions
 */
public class SessionManager {

    private static ConcurrentMap<IODevice, SessionManager> DEVICE_MAP = new ConcurrentHashMap<>();

    private IODevice device;
    private Map<Byte, SimonSession> sessions = new HashMap<>();

    SessionManager(IODevice device) {
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

    /**
     * Creates or finds a SessionManager for the given communication device
     *
     * @param device the device to lookup, cannot be null
     * @return the existing SessionManager or a new session manager for the device
     */
    public static SessionManager forDevice(IODevice device) {
        if (device == null) throw new IllegalArgumentException("Communication device is required");
        if (!DEVICE_MAP.containsKey(device))
            DEVICE_MAP.put(device, new SessionManager(device));
        return DEVICE_MAP.get(device);
    }

}
