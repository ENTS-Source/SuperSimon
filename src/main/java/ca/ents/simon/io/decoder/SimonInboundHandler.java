package ca.ents.simon.io.decoder;

import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.impl.DiscoverCommand;
import ca.ents.simon.io.device.IODevice;
import ca.ents.simon.io.session.SessionManager;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;

/**
 * Protocol handler for "SuperSimon" protocol defined by ENTS
 */
public class SimonInboundHandler extends SimpleChannelInboundHandler<SimonCommand> {

    private IODevice device;

    public SimonInboundHandler(IODevice device) {
        if (device == null) throw new IllegalArgumentException("IO device cannot be null");
        this.device = device;
    }

    @Override
    protected void channelRead0(ChannelHandlerContext channelHandlerContext, SimonCommand simonCommand) throws Exception {
        SessionManager.forDevice(device).createOrFindSession(simonCommand.getReceivingAddress()).handleCommand(simonCommand);
    }

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        // TODO: Figure out why this needs to occur
        // This is needed otherwise the channel does not become active
        ctx.channel().writeAndFlush(new DiscoverCommand((byte) 0xFF)).sync();
    }
}
