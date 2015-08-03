package ca.ents.simon.io.decoder;

import ca.ents.simon.io.CommandRegistry;
import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.ReplayingDecoder;
import sun.plugin.dom.exception.InvalidStateException;

import java.util.ArrayList;
import java.util.List;

/**
 * Protocol decoder for "SuperSimon" protocol defined by ENTS
 */
public class SimonDecoder extends ReplayingDecoder<SimonDecoder.DecoderState> {

    // Outgoing sequence
    //private final static byte[] MAGIC_SEQUENCE = {0xD, 0xE, 0xA, 0xD, 0xB, 0xE, 0xE, 0xF};
    private final static byte[] MAGIC_SEQUENCE = {0xC, 0xA, 0xF, 0xE, 0xB, 0xA, 0xB, 0xE};

    private byte commandId;
    private byte address;
    private int length;
    private List<Byte> payload = new ArrayList<>();

    public SimonDecoder() {
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
                        if (magicHeader[i] != MAGIC_SEQUENCE[i])
                            throw new InvalidStateException("Invalid magic sequence header. Expected " + MAGIC_SEQUENCE[i] + " but got " + magicHeader[i]);
                    }

                    // Header validated, read address and command ID
                    address = in.readByte();
                    commandId = in.readByte();

                    CommandRegistry.CommandInfo currentCommand = CommandRegistry.getCommandInfo(commandId);
                    if (currentCommand.hasPayload()) {
                        checkpoint(DecoderState.LENGTH_CHECKPOINT);
                    } else {
                        // TODO: Decode command and add to 'out'
                        checkpoint(DecoderState.MAGIC_CHECKPOINT);
                    }
                    break;
                case LENGTH_CHECKPOINT:
                    if (in.readableBytes() < 4) return; // Nothing to do
                    length = in.readInt();
                    payload.clear();
                    checkpoint(DecoderState.PAYLOAD_CHECKPOINT);
                    break;
                case PAYLOAD_CHECKPOINT:
                    payload.add(in.readByte());
                    checkpoint(DecoderState.PAYLOAD_CHECKPOINT);
                    if (payload.size() == length) {
                        // TODO: Decode command and add to 'out'
                        checkpoint(DecoderState.MAGIC_CHECKPOINT);
                    }
                    break;
                default:
                    throw new IllegalStateException("Invalid decoder state");
            }
        }
    }

    enum DecoderState {MAGIC_CHECKPOINT, LENGTH_CHECKPOINT, PAYLOAD_CHECKPOINT}
}
