package ca.ents.simon.io.command;

/**
 * Represents a SuperSimon communication command
 */
public abstract class SimonCommand {
    private byte address;

    public SimonCommand(byte receivedForAddress) {
        this.address = receivedForAddress;
    }

    public byte getReceivingAddress() {
        return address;
    }
}
