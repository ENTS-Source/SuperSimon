package ca.ents.simon.io.command;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Represents a communication command for SuperSimon
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Command {
    /**
     * The command ID for this command
     * @return the command ID
     */
    byte value();

    /**
     * Whether or not this command has a payload
     * @return true if there is a payload, false otherwise
     */
    boolean hasPayload() default  false;

}
