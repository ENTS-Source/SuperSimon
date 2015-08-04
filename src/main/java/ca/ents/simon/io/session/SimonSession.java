package ca.ents.simon.io.session;

import ca.ents.simon.io.command.SimonCommand;
import io.netty.channel.Channel;

/**
 * A session on the communication device
 */
public class SimonSession {

    private byte address;
    private Channel channel;
    private boolean validSession = true;
    private long lastSend = 0; // Non-zero if pending response

    public SimonSession(byte address, Channel channel) {
        if (channel == null) throw new IllegalArgumentException("Channel cannot be null for a session");
        this.address = address;
        this.channel = channel;
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
     * Sends a command to this session
     *
     * @param command the command to send to the session, cannot be null
     */
    public void sendCommand(SimonCommand command) {
        // TODO: Some kind of (non-)blocking queue?
        if (command == null) throw new IllegalArgumentException("Command to send cannot be null");
        lastSend = System.currentTimeMillis();
        channel.writeAndFlush(command);
    }

    // TODO: Hook up sessions to actual IO processing
    // TODO: Handle incoming commands for this address
    // TODO: Handle timeout for response (if applicable)
    // TODO: Handle responses to commands (and lack of compliance)

}
