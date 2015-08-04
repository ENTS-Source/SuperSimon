package ca.ents.simon.io;

import ca.ents.simon.io.command.Command;
import ca.ents.simon.io.command.SimonCommand;
import org.reflections.Reflections;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Registry for all commands within the SuperSimon protocol
 */
public final class CommandRegistry {

    private static Map<Class<? extends SimonCommand>, Byte> BY_CLASS = new HashMap<>();
    private static Map<Byte, Class<? extends SimonCommand>> BY_ID = new HashMap<>();
    private static Map<Byte, Command> ANNOTATION_INSTANCES = new HashMap<>();

    static {
        // Find all commands and register them
        Reflections reflections = new Reflections("ca.ents.simon");
        Set<Class<?>> hasAnnotation = reflections.getTypesAnnotatedWith(Command.class);
        for (Class<?> type : hasAnnotation) {
            if (!SimonCommand.class.isAssignableFrom(type)) {
                throw new IllegalStateException("Type " + type.getName() + " has the Command annotation but is not a SimonCommand");
            } else {
                // TODO: Ensure safety of casting here
                Class<? extends SimonCommand> commandClass = (Class<? extends SimonCommand>) type;
                Command annotation = type.getAnnotation(Command.class);
                ANNOTATION_INSTANCES.put(annotation.commandId(), annotation);
                BY_ID.put(annotation.commandId(), commandClass);
                BY_CLASS.put(commandClass, annotation.commandId());
            }
        }
        System.out.println("Registered " + BY_ID.size() + " commands");
    }

    private CommandRegistry() {
    }

    /**
     * Retrieves command information for a given command. If the command is not found then
     * an exception is raised
     *
     * @param commandId the command ID to lookup
     * @return the command info found
     */
    public static CommandInfo getCommandInfo(byte commandId) {
        if (!BY_ID.containsKey(commandId))
            throw new IllegalArgumentException("Command '" + commandId + "' does not exist");
        return new CommandInfo(ANNOTATION_INSTANCES.get(commandId), BY_ID.get(commandId));
    }

    /**
     * Retrieves command information for a given command. If the command is not found then
     * an exception is raised
     *
     * @param command the command class to lookup
     * @return the command info found
     */
    public static CommandInfo getCommandInfo(Class<? extends SimonCommand> command) {
        if (!BY_CLASS.containsKey(command))
            throw new IllegalArgumentException("Command '" + command.getName() + "' does not exist");
        return getCommandInfo(BY_CLASS.get(command));
    }

}
