package ca.ents.simon.io.decoder;

import ca.ents.simon.io.CommandInfo;
import ca.ents.simon.io.CommandRegistry;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.payload.PayloadEncoderDecoder;
import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.MessageToMessageEncoder;

import java.util.Collections;
import java.util.List;

/**
 * Simon command encoder
 */
public class SimonEncoder extends MessageToMessageEncoder<SimonCommand> {

    private final static byte[] MAGIC_SEQUENCE = {0xD, 0xE, 0xA, 0xD, 0xB, 0xE, 0xE, 0xF}; // 0xDEADBEEF

    @SuppressWarnings("unchecked")
    @Override
    protected void encode(ChannelHandlerContext ctx, SimonCommand command, List<Object> out) throws Exception {
        CommandInfo cmdInfo = CommandRegistry.getCommandInfo(command.getClass());
        Collections.addAll(out, MAGIC_SEQUENCE);
        out.add(command.getAddress());
        out.add(cmdInfo.getCommandId());

        if (cmdInfo.hasPayload()) {
            PayloadEncoderDecoder payloadEncoder = cmdInfo.getPayloadEncoderDecoder();
            ByteBuf payload = payloadEncoder.encode(command);
            byte[] payloadRaw = payload.array();
            out.add(payloadRaw.length);
            Collections.addAll(out, payloadRaw);
        }
    }
}
