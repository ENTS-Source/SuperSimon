package ca.ents.simon.io.command;

import org.reflections.Reflections;

import java.util.*;

/**
 * Registry for all commands within the SuperSimon protocol
 */
public final class CommandRegistry {

    private static Map<Class<? extends SimonCommand>, CommandInfo> BY_CLASS = new HashMap<>();
    private static Map<Byte, CommandInfo> BY_ID = new HashMap<>();

    static {
        // Find all commands and register them
        Reflections reflections = new Reflections("ca.ents.simon");
        Set<Class<?>> hasAnnotation = reflections.getTypesAnnotatedWith(Command.class);
        for (Class<?> type : hasAnnotation) {
            if (!SimonCommand.class.isAssignableFrom(type)) {
                throw new IllegalStateException("Type " + type.getName() + " has the Command annotation but is not a SimonCommand");
            } else {
                @SuppressWarnings("unchecked") Class<? extends SimonCommand> commandClass = (Class<? extends SimonCommand>) type;

                Command annotation = type.getAnnotation(Command.class);

                RequiresResponse[] responses = type.getAnnotationsByType(RequiresResponse.class);
                List<Class<? extends SimonCommand>> requiresResponses = new ArrayList<>();
                for (RequiresResponse respAnnotation : responses)
                    requiresResponses.add(respAnnotation.value());

                CommandInfo info = new CommandInfo(annotation, commandClass, requiresResponses);

                BY_CLASS.put(commandClass, info);
                BY_ID.put(annotation.commandId(), info);
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
        return BY_ID.get(commandId);
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
        return BY_CLASS.get(command);
    }

}
