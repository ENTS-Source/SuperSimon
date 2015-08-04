package ca.ents.simon.io.decoder;

import ca.ents.simon.io.command.impl.EchoCommand;
import ca.ents.simon.io.command.SimonCommand;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;

// TODO: Docs and implementation
public class SimonInboundHandler extends SimpleChannelInboundHandler<SimonCommand> {
    @Override
    protected void channelRead0(ChannelHandlerContext channelHandlerContext, SimonCommand simonCommand) throws Exception {
        System.out.println("GOT COMMAND: " + simonCommand);
        // TODO: Actually handle command
    }

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        // TODO: Raise event for application start
        EchoCommand command = new EchoCommand((byte) 0x03);
        command.generatePayload();
        ChannelFuture future = ctx.writeAndFlush(command).sync();
        if (!future.isSuccess())
            future.cause().printStackTrace();
    }
}
