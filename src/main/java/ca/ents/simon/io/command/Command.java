package ca.ents.simon.io.command;

import ca.ents.simon.io.command.init.CommandInitializer;
import ca.ents.simon.io.payload.NoPayloadEncoderDecoder;
import ca.ents.simon.io.payload.PayloadEncoderDecoder;

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
     *
     * @return the command ID
     */
    byte value();

    /**
     * Whether or not this command has a payload
     *
     * @return true if there is a payload, false otherwise
     */
    boolean hasPayload() default false;

    /**
     * The encoder/decoder to use for the payload, if required
     *
     * @return the encoder/decoder class for the payload
     */
    Class<? extends PayloadEncoderDecoder> payloadEncoder() default NoPayloadEncoderDecoder.class;

    /**
     * The initializer for this command
     *
     * @return the initializer for this command
     */
    Class<? extends CommandInitializer> initializer();

}
