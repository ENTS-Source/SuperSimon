package ca.ents.simon.io.decoder;

import ca.ents.simon.io.CommandInfo;
import ca.ents.simon.io.CommandRegistry;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.init.CommandInitializer;
import ca.ents.simon.io.payload.PayloadEncoderDecoder;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.MessageToMessageDecoder;

import java.util.List;

/**
 * Simon command decoder
 */
public class SimonDecoder extends MessageToMessageDecoder<FrameInfo> {
    @SuppressWarnings("unchecked")
    @Override
    protected void decode(ChannelHandlerContext ctx, FrameInfo frame, List<Object> out) throws Exception {
        CommandInfo cmdInfo = CommandRegistry.getCommandInfo(frame.getCommandId());
        CommandInitializer initializer = cmdInfo.getInitializer();

        SimonCommand command = initializer.createCommand(frame.getAddress());

        if (cmdInfo.hasPayload()) {
            PayloadEncoderDecoder payloadDecoder = cmdInfo.getPayloadEncoderDecoder();
            payloadDecoder.decode(frame.getPayload(), command);
        }

        System.out.println("RECV");
        System.out.println(command.toString());

        out.add(command);
    }
}
