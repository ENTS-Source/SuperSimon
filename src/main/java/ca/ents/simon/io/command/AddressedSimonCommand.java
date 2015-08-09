package ca.ents.simon.io.command;

/**
 * Represents an addressed SuperSimon communication command
 */
public class AddressedSimonCommand extends SimonCommand {

    private byte address;

    /**
     * Creates a new command that is targeted at the given address
     *
     * @param address the target address
     */
    public AddressedSimonCommand(byte address) {
        super(address);
        this.address = address;
    }

    /**
     * Gets the address this command is targeted at
     *
     * @return the destination address
     */
    public byte getTargetAddress() {
        return address;
    }
}
