package ca.ents.simon.io.command;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Indicates that a command requires a particular response command in order to function
 * correctly.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface RequiresResponse {
    /**
     * The command that must be sent back in order to be considered a valid response
     *
     * @return the type of command response
     */
    Class<? extends SimonCommand> value();
}
