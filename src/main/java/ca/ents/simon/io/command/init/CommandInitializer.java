package ca.ents.simon.io.command.init;

import ca.ents.simon.io.command.SimonCommand;

/**
 * A Simon command initializer
 */
public interface CommandInitializer<T extends SimonCommand> {
    /**
     * Creates a new Simon command for the given address with no current payload.
     * The payload will be appended at a later time.
     *
     * @param forAddress the target address
     * @return the created command
     */
    T createCommand(byte forAddress);
}
