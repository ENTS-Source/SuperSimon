package ca.ents.simon.io.command;

import java.util.Arrays;

/**
 * Represents a SuperSimon command that carries a payload
 */
public abstract class PayloadCarryingSimonCommand extends SimonCommand {

    private byte[] payload;

    public PayloadCarryingSimonCommand(byte address, byte[] payload) {
        super(address);
        this.payload = Arrays.copyOf(payload, payload.length);
    }

    /**
     * Gets a clone of this command's payload
     *
     * @return a copy of this command's payload
     */
    public byte[] getPayload() {
        return Arrays.copyOf(payload, payload.length);
    }
}
