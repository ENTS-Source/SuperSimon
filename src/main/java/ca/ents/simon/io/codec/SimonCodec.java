package ca.ents.simon.io.codec;

import ca.ents.simon.io.command.PayloadCarryingSimonCommand;
import ca.ents.simon.io.command.SimonCommand;
import io.netty.buffer.ByteBuf;

/**
 * Represents a command codec
 */
public abstract class SimonCodec<T extends SimonCommand> {

    // TODO: This might be better replaced with an encoder/decoder at the netty level
    // For example:
    // - Framing sends along a "frame info" object to decoder
    // - Decoder builds command and sends command along
    // - Internal logic sends a command back (assumption)
    // - Encoder builds command, including magic value and headers

    // I don't know where else to put this to-do, so here it goes...
    // TODO: Some kind of "requires response" handling (ie: @RequiresResponse(returnCommand=AckCommand.class))

    public abstract T decode(ByteBuf buffer);

    public abstract ByteBuf encode(T command);

    protected byte readAddress(ByteBuf buffer) {
        byte address = buffer.readByte();
        return address;
    }

    protected byte[] readPayload(ByteBuf buffer) {
        int length = buffer.readInt();
        byte[] payload = new byte[length];
        buffer.readBytes(payload);
        return payload;
    }

    protected void writeAddress(SimonCommand command, ByteBuf buffer) {
        buffer.writeByte(command.getAddress());
    }

    protected void writePayload(PayloadCarryingSimonCommand command, ByteBuf buffer) {
        byte[] payload = command.getPayload();
        buffer.writeInt(payload.length);
        buffer.writeBytes(payload);
    }
}
