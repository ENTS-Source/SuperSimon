package ca.ents.simon.io.decoder;

import ca.ents.simon.io.command.CommandInfo;
import ca.ents.simon.io.command.CommandRegistry;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.payload.PayloadEncoderDecoder;
import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.MessageToByteEncoder;

import java.nio.ByteOrder;

/**
 * Simon command encoder
 */
public class SimonEncoder extends MessageToByteEncoder<SimonCommand> {

    private final static byte[] MAGIC_SEQUENCE = {(byte) 0xDE, (byte) 0xAD, (byte) 0xBE, (byte) 0xEF}; // 0xDEADBEEF

    @SuppressWarnings("unchecked")
    @Override
    protected void encode(ChannelHandlerContext ctx, SimonCommand command, ByteBuf out) throws Exception {
        CommandInfo cmdInfo = CommandRegistry.getCommandInfo(command.getClass());
        out.writeBytes(MAGIC_SEQUENCE);
        out.writeByte(cmdInfo.getCommandId());
        out.writeByte(command.getAddress());

        if (cmdInfo.hasPayload()) {
            PayloadEncoderDecoder payloadEncoder = cmdInfo.getPayloadEncoderDecoder();
            ByteBuf payload = payloadEncoder.encode(command);
            byte[] payloadRaw = new byte[payload.readableBytes()];
            payload.readBytes(payloadRaw);
            out.writeInt(payloadRaw.length);
            out.writeBytes(payloadRaw);
        }

        // So that netty can read our bytes
        out.order(ByteOrder.BIG_ENDIAN);
        out.readerIndex(0);
    }
}
