package ca.ents.simon.io.session;

import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.impl.DiscoverCommand;

/**
 * A session on the communication device
 */
public class SimonSession {

    private byte address;
    private SessionManager manager;

    private boolean online = false;

    SimonSession(byte address, SessionManager manager) {
        this.manager = manager;
        this.address = address;
    }

    /**
     * Gets the address of this session
     *
     * @return the session address
     */
    public byte getAddress() {
        return address;
    }

    /**
     * Processes a SimonCommand for handling. May not be processed immediately. This is non-blocking.
     *
     * @param command the command to process, cannot be null
     */
    public void handleCommand(SimonCommand command) {
        if (command == null) throw new IllegalArgumentException("Command to handle cannot be null");
        manager.handleCommand(command);
    }

    /**
     * Sends a command to this session
     *
     * @param command the command to send to the session, cannot be null
     */
    public void sendCommand(SimonCommand command) {
        if (command == null) throw new IllegalArgumentException("Command to send cannot be null");
        manager.sendCommand(command);
    }

    /**
     * Attempts a discovery on this session
     */
    public void tryDiscover() {
        sendCommand(new DiscoverCommand(address));
    }

    /**
     * Gets whether or not this session is considered online and responding correctly
     * to the protocol
     *
     * @return true if online, false otherwise
     */
    public boolean isOnline() {
        return online;
    }

    void setOnline(boolean online) {
        this.online = online;
        // TODO: Player offline/online event
    }

    @Override
    public String toString() {
        return "SimonSession{" + "address=" + address + ", online=" + online + "}";
    }
}
