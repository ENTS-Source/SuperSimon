package ca.ents.simon.io.command;

/**
 * Represents a SuperSimon communication command
 */
public abstract class SimonCommand {

    private byte address;

    public SimonCommand(byte address) {
        this.address = address;
    }

    public byte getAddress() {
        return address;
    }
}
