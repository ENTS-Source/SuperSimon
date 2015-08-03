package ca.ents.simon.io.decoder;

import ca.ents.simon.io.CommandInfo;
import ca.ents.simon.io.CommandRegistry;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.ReplayingDecoder;

import java.util.List;

/**
 * Protocol decoder for "SuperSimon" protocol defined by ENTS
 */
public class SimonFrameDecoder extends ReplayingDecoder<SimonFrameDecoder.DecoderState> {

    private final static byte[] MAGIC_SEQUENCE = {0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE}; // 0xCAFEBABE

    private byte commandId;
    private byte address;
    private int length;
    private int currentPayloadLength;
    private ByteBuf payload;

    public SimonFrameDecoder() {
        super(DecoderState.MAGIC_CHECKPOINT);
    }

    @Override
    protected void decode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out) throws Exception {
        // TODO: Finish framing
        while (in.readableBytes() > 0) {
            switch (state()) {
                case MAGIC_CHECKPOINT:
                    if (in.readableBytes() < MAGIC_SEQUENCE.length + 2) return; // Nothing to do

                    // Attempt to validate magic header
                    byte[] magicHeader = new byte[MAGIC_SEQUENCE.length];
                    in.readBytes(magicHeader);
                    for (int i = 0; i < magicHeader.length; i++) {
                        if (magicHeader[i] != MAGIC_SEQUENCE[i]) {
                            System.out.println("Invalid magic sequence header. Expected " + MAGIC_SEQUENCE[i] + " but got " + magicHeader[i]);

                            // Dispose of data and exit: invalid sequence
                            checkpoint(DecoderState.MAGIC_CHECKPOINT);
                            return;
                        }
                    }

                    // Header validated, read address and command ID
                    address = in.readByte();
                    commandId = in.readByte();

                    CommandInfo currentCommand = CommandRegistry.getCommandInfo(commandId);
                    if (currentCommand.hasPayload()) {
                        checkpoint(DecoderState.LENGTH_CHECKPOINT);
                    } else {
                        out.add(new FrameInfo(commandId, address));
                        checkpoint(DecoderState.MAGIC_CHECKPOINT);
                    }
                    break;
                case LENGTH_CHECKPOINT:
                    if (in.readableBytes() < 4) return; // Nothing to do
                    length = in.readInt();
                    payload = Unpooled.buffer(length);
                    currentPayloadLength = 0;
                    checkpoint(DecoderState.PAYLOAD_CHECKPOINT);
                    break;
                case PAYLOAD_CHECKPOINT:
                    payload.writeByte(in.readByte());
                    currentPayloadLength++;
                    checkpoint(DecoderState.PAYLOAD_CHECKPOINT);
                    if (currentPayloadLength == length) {
                        out.add(new FrameInfo(commandId, address, payload));
                        checkpoint(DecoderState.MAGIC_CHECKPOINT);
                    }
                    break;
                default:
                    throw new IllegalStateException("Invalid decoder state: " + state());
            }
        }
    }

    enum DecoderState {MAGIC_CHECKPOINT, LENGTH_CHECKPOINT, PAYLOAD_CHECKPOINT}
}
