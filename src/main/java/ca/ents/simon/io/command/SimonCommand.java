package ca.ents.simon.io.command;

/**
 * Represents a SuperSimon communication command
 */
public abstract class SimonCommand {

    private byte address = (byte) 0xFF;

    /**
     * Creates a new Simon command that was not received
     */
    public SimonCommand() {
    }

    /**
     * Creates a new Simon command that was received from an address
     *
     * @param receivedForAddress the address that sent the command
     */
    public SimonCommand(byte receivedForAddress) {
        this.address = receivedForAddress;
    }

    /**
     * Gets the received address, if present. Returns 0xFF if this command
     * was not received
     *
     * @return the received address
     */
    public byte getReceivingAddress() {
        return address;
    }
}
