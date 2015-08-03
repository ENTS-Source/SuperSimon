package ca.ents.simon.io.payload;

import ca.ents.simon.io.command.SimonCommand;
import io.netty.buffer.ByteBuf;

import static io.netty.buffer.Unpooled.buffer;

/**
 * Default payload encoder/decoder that does not handle any payload. Encoding will return a 0-length
 * buffer while decoding will do nothing.
 */
public class NoPayloadEncoderDecoder implements PayloadEncoderDecoder<SimonCommand> {
    @Override
    public ByteBuf encode(SimonCommand command) {
        return buffer(0);
    }

    @Override
    public void decode(ByteBuf payload, SimonCommand command) {
        // Nothing to do
    }
}
