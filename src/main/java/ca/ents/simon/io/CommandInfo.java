package ca.ents.simon.io;

import ca.ents.simon.io.command.Command;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.init.CommandInitializer;
import ca.ents.simon.io.payload.PayloadEncoderDecoder;

/**
 * Command information carrier for command registry
 */
public class CommandInfo {

    private Class<? extends SimonCommand> commandClass;
    private Command annotation;

    CommandInfo(Command annotation, Class<? extends SimonCommand> clazz) {
        this.commandClass = clazz;
        this.annotation = annotation;
    }

    /**
     * Determines whether or not this command requires a payload
     *
     * @return true if a payload is required, false otherwise
     */
    public boolean hasPayload() {
        return annotation.hasPayload();
    }

    /**
     * Gets the command ID for this command
     *
     * @return the command ID
     */
    public byte getCommandId() {
        return annotation.commandId();
    }

    /**
     * Gets the payload encoder/decoder for this command. If this command does not support
     * a payload then this returns null.
     *
     * @return the payload encoder/decoder
     */
    public PayloadEncoderDecoder getPayloadEncoderDecoder() {
        if (!hasPayload()) return null;
        try {
            return annotation.payloadEncoder().newInstance();
        } catch (InstantiationException | IllegalAccessException e) {
            throw new RuntimeException("Could not create payload encoder/decoder", e);
        }
    }

    /**
     * Gets the command initializer for this command
     *
     * @return the command initializer
     */
    public CommandInitializer getInitializer() {
        try {
            return annotation.initializer().newInstance();
        } catch (InstantiationException | IllegalAccessException e) {
            throw new RuntimeException("Could not create payload encoder/decoder", e);
        }
    }
}
