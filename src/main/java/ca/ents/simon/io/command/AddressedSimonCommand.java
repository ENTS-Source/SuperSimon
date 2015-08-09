package ca.ents.simon.io.command;

/**
 * Represents an addressed SuperSimon communication command
 */
public class AddressedSimonCommand extends SimonCommand {
    private byte address;

    public AddressedSimonCommand(byte address) {
        super(address);
        this.address = address;
    }

    public byte getAddress() {
        return address;
    }
}
