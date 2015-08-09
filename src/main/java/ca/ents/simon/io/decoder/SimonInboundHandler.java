package ca.ents.simon.io.decoder;

import ca.ents.simon.io.Communication;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.impl.DiscoverCommand;
import ca.ents.simon.io.device.IODevice;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;

// TODO: Docs and implementation
public class SimonInboundHandler extends SimpleChannelInboundHandler<SimonCommand> {

    private IODevice device;

    public SimonInboundHandler(IODevice device) {
        if (device == null) throw new IllegalArgumentException("IO device cannot be null");
        this.device = device;
    }

    @Override
    protected void channelRead0(ChannelHandlerContext channelHandlerContext, SimonCommand simonCommand) throws Exception {
        System.out.println("GOT COMMAND: " + simonCommand);
        Communication.forDevice(device).createOrFindSession(simonCommand.getAddress()).handleCommand(simonCommand);
    }

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        // TODO: Raise event for application start
        System.out.println("Channel active!");
        // This is needed otherwise the channel does not become active
        ctx.channel().writeAndFlush(new DiscoverCommand((byte) 0xFF)).sync();
    }
}
