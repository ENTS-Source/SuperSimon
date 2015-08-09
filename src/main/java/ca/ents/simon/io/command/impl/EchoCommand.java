package ca.ents.simon.io.command.impl;

import ca.ents.simon.io.command.Command;
import ca.ents.simon.io.command.RequiresResponse;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.init.EchoCommandInitializer;
import ca.ents.simon.io.payload.impl.EchoCommandPayloadEncoderDecoder;

import java.util.Arrays;
import java.util.Random;

/**
 * Sends a payload for the client to send back in-tact. Return address should be the first
 * byte of the payload.
 */
@Command(commandId = (byte) 0xF0, hasPayload = true, initializer = EchoCommandInitializer.class, payloadEncoder = EchoCommandPayloadEncoderDecoder.class)
@RequiresResponse(EchoCommand.class)
public class EchoCommand extends SimonCommand {

    private byte[] payload;

    public EchoCommand(byte address) {
        super(address);
    }

    /**
     * Generates a random payload for this command
     */
    public void generatePayload() {
        Random random = new Random();
        payload = new byte[random.nextInt(20) + 1];
        for (int i = 0; i < payload.length; i++) {
            payload[i] = (byte) random.nextInt(255);
        }
    }

    /**
     * Gets an immutable copy of this command's payload
     *
     * @return an immutable copy of the payload
     */
    public byte[] getPayload() {
        return Arrays.copyOf(payload, payload.length);
    }

    /**
     * Sets the payload for this command
     *
     * @param payload the payload to use, cannot be null and must contain at least 1 entry
     */
    public void setPayload(byte[] payload) {
        if (payload == null || payload.length < 1)
            throw new IllegalArgumentException("Payload must not be null and must contain at least 1 byte");
        this.payload = Arrays.copyOf(payload, payload.length);
    }
}
