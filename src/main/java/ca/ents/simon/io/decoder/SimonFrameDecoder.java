package ca.ents.simon.io.decoder;

import ca.ents.simon.io.command.CommandInfo;
import ca.ents.simon.io.command.CommandRegistry;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.init.CommandInitializer;
import ca.ents.simon.io.payload.PayloadEncoderDecoder;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.ReplayingDecoder;

import java.util.ArrayList;
import java.util.List;

/**
 * Protocol decoder for "SuperSimon" protocol defined by ENTS
 */
public class SimonFrameDecoder extends ReplayingDecoder<SimonFrameDecoder.DecoderState> {

    private final static byte[] MAGIC_SEQUENCE = {(byte) 0xCA, (byte) 0xFE, (byte) 0xBA, (byte) 0xBE}; // 0xCAFEBABE

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
        List<FrameInfo> frames = new ArrayList<>();
        boolean continueRead = true;
        while (in.readableBytes() > 0 && continueRead) {
            switch (state()) {
                case MAGIC_CHECKPOINT:
                    if (in.readableBytes() < MAGIC_SEQUENCE.length + 2) continueRead = false; // Nothing to do
                    else {
                        // Attempt to validate magic header
                        byte[] magicHeader = new byte[MAGIC_SEQUENCE.length];
                        in.readBytes(magicHeader);
                        for (int i = 0; i < magicHeader.length; i++) {
                            if (magicHeader[i] != MAGIC_SEQUENCE[i]) {
                                System.out.println("Invalid magic sequence header. Expected " + MAGIC_SEQUENCE[i] + " but got " + magicHeader[i]);

                                // Dispose of data and exit: invalid sequence
                                checkpoint(DecoderState.MAGIC_CHECKPOINT);
                                continueRead = false;
                            }
                        }

                        if (continueRead) {

                            // Header validated, read address and command ID
                            commandId = in.readByte();
                            CommandInfo currentCommand = CommandRegistry.getCommandInfo(commandId);

                            if (commandId != 0)
                                address = in.readByte();
                            else
                                address = 0x03; // TODO: Remove workaround and actually implement something proper for this scenario

                            if (currentCommand.hasPayload()) {
                                checkpoint(DecoderState.LENGTH_CHECKPOINT);
                            } else {
                                frames.add(new FrameInfo(commandId, address));
                                checkpoint(DecoderState.MAGIC_CHECKPOINT);
                                continueRead = false; // TODO: Need to figure out why setting the checkpoint causes an exception in the magic read code
                            }
                        }
                    }
                    break;
                case LENGTH_CHECKPOINT:
                    if (in.readableBytes() < 4) continueRead = false; // Nothing to do
                    else {
                        length = in.readInt();
                        payload = Unpooled.buffer(length);
                        currentPayloadLength = 0;
                        checkpoint(DecoderState.PAYLOAD_CHECKPOINT);
                    }
                    break;
                case PAYLOAD_CHECKPOINT:
                    payload.writeByte(in.readByte());
                    currentPayloadLength++;
                    checkpoint(DecoderState.PAYLOAD_CHECKPOINT);
                    if (currentPayloadLength == length) {
                        frames.add(new FrameInfo(commandId, address, payload));
                        checkpoint(DecoderState.MAGIC_CHECKPOINT);
                        continueRead = false; // TODO: Need to figure out why setting the checkpoint causes an exception in the magic read code
                    }
                    break;
                default:
                    throw new IllegalStateException("Invalid decoder state: " + state());
            }
        }

        for (FrameInfo frame : frames)
            handleFrame(frame, out);
    }

    @SuppressWarnings("unchecked")
    private void handleFrame(FrameInfo frame, List<Object> out) {
        CommandInfo cmdInfo = CommandRegistry.getCommandInfo(frame.getCommandId());
        CommandInitializer initializer = cmdInfo.getInitializer();

        SimonCommand command = initializer.createCommand(frame.getAddress());

        if (cmdInfo.hasPayload()) {
            PayloadEncoderDecoder payloadDecoder = cmdInfo.getPayloadEncoderDecoder();
            payloadDecoder.decode(frame.getPayload(), command);
        }

        out.add(command);
    }

    enum DecoderState {MAGIC_CHECKPOINT, LENGTH_CHECKPOINT, PAYLOAD_CHECKPOINT}
}
