package ca.ents.simon.io.command.init;

import ca.ents.simon.io.command.SimonCommand;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.ParameterizedType;

/**
 * Command initializer for commands that have a single constructor available that
 * accepts 1 byte as the address.
 */
public abstract class SimpleCommandInitializer<T extends SimonCommand> implements CommandInitializer<T> {

    @SuppressWarnings("unchecked")
    @Override
    public T createCommand(byte forAddress) {
        Class<?> commandClass = getGenericClass();
        try {
            Constructor<?> constructor = commandClass.getConstructor(byte.class);
            return (T) constructor.newInstance(forAddress);
        } catch (NoSuchMethodException | InvocationTargetException | InstantiationException | IllegalAccessException e) {
            throw new RuntimeException("Failed to create command of type " + commandClass.getName(), e);
        }
    }

    private Class<?> getGenericClass() {
        return (Class) ((ParameterizedType) getClass().getGenericSuperclass()).getActualTypeArguments()[0];
    }
}
