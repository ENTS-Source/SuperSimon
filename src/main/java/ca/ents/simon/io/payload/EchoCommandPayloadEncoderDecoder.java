package ca.ents.simon.io.payload;

import ca.ents.simon.io.command.EchoCommand;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;

/**
 * Payload encoder/decoder for the echo command
 */
public class EchoCommandPayloadEncoderDecoder implements PayloadEncoderDecoder<EchoCommand> {
    @Override
    public ByteBuf encode(EchoCommand command) {
        ByteBuf buffer = Unpooled.buffer();
        buffer.writeBytes(command.getPayload());
        buffer.readerIndex(0);
        return buffer;
    }

    @Override
    public void decode(ByteBuf payload, EchoCommand command) {
        byte[] payloadArray = new byte[payload.readableBytes()];
        payload.readBytes(payloadArray);
        command.setPayload(payloadArray);
    }
}
