package ca.ents.simon.io.payload;

import ca.ents.simon.io.command.SimonCommand;
import io.netty.buffer.ByteBuf;

/**
 * Encoder/decoder for payloads
 */
public interface PayloadEncoderDecoder<T extends SimonCommand> {
    /**
     * Encodes a particular command's payload into a byte buffer
     *
     * @param command the command to encode, should not be null
     * @return the encoded payload as a byte buffer
     */
    ByteBuf encode(T command);

    /**
     * Decodes the given payload into the given command. Implementations may clear
     * any payload on the command before decoding or append data to the command.
     *
     * @param payload the payload to decode, should not be null
     * @param command the command to decode the payload into, should not be null
     */
    void decode(ByteBuf payload, T command);
}
