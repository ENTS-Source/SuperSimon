package ca.ents.simon.io.command;

import ca.ents.simon.io.command.init.CommandInitializer;
import ca.ents.simon.io.payload.PayloadEncoderDecoder;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

/**
 * Command information carrier for command registry
 */
public class CommandInfo {

    private Class<? extends SimonCommand> commandClass;
    private Command annotation;
    private List<Class<? extends SimonCommand>> responseCommandClasses = new ArrayList<>();

    CommandInfo(Command annotation, Class<? extends SimonCommand> clazz, Collection<Class<? extends SimonCommand>> requiredResponses) {
        this.commandClass = clazz;
        this.annotation = annotation;
        this.responseCommandClasses.addAll(requiredResponses);
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

    /**
     * Gets the response command classes that are valid to receive when this command is sent
     *
     * @return an immutable collection of command response classes that are valid to receive back, may be empty
     */
    public List<Class<? extends SimonCommand>> getValidResponseClasses() {
        return Collections.unmodifiableList(responseCommandClasses);
    }

    /**
     * Gets the class of this command
     *
     * @return the class of the command
     */
    public Class<? extends SimonCommand> getCommandClass() {
        return commandClass;
    }
}
