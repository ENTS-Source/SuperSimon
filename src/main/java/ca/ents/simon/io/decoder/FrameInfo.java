package ca.ents.simon.io.decoder;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;

/**
 * A frame of data from the IO device representing one Simon command
 */
public class FrameInfo {

    private byte commandId;
    private byte address;
    private ByteBuf payload;

    public FrameInfo(byte commandId, byte address) {
        this(commandId, address, Unpooled.buffer(0));
    }

    public FrameInfo(byte commandId, byte address, ByteBuf payload) {
        if (payload == null) throw new IllegalArgumentException("Payload cannot be null");

        this.commandId = commandId;
        this.address = address;
        this.payload = payload;

        this.payload.readerIndex(0);
    }

    /**
     * Gets the command ID associated with this frame
     *
     * @return the command ID
     */
    public byte getCommandId() {
        return commandId;
    }

    /**
     * Gets the address associated with this frame
     *
     * @return the address
     */
    public byte getAddress() {
        return address;
    }

    /**
     * Gets the raw payload associated with this frame. May return a 0-length buffer
     * if no payload. Should never return null.
     *
     * @return the raw payload
     */
    public ByteBuf getPayload() {
        return payload;
    }

    /**
     * Determines whether or not this frame contains a payload
     *
     * @return true if this frame is carrying a payload, false otherwise
     */
    public boolean hasPayload() {
        return payload.capacity() > 0;
    }
}
