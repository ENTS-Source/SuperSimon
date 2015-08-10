package ca.ents.simon.io.decoder;

import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.impl.DiscoverCommand;
import ca.ents.simon.io.device.IODevice;
import ca.ents.simon.io.session.SessionManager;
import com.beauhinks.purejavacomm.PureJavaCommChannel;
import io.netty.channel.Channel;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import purejavacomm.SerialPort;

import java.lang.reflect.Field;

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
        System.out.println("[Netty] Received command: " + simonCommand);
        SessionManager.forDevice(device).createOrFindSession(simonCommand.getReceivingAddress()).handleCommand(simonCommand);
    }

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        Channel channel = ctx.channel();
        if (channel instanceof PureJavaCommChannel) {
            // HACK: This is a workaround to ensure that the client doesn't block for all eternity
            PureJavaCommChannel serialPort = (PureJavaCommChannel) channel;
            Field field = serialPort.getClass().getDeclaredField("serialPort");
            field.setAccessible(true);
            SerialPort sp = (SerialPort) field.get(serialPort);
            sp.enableReceiveTimeout(1000);
        }
        // TODO: Figure out why this needs to occur
        // This is needed otherwise the channel does not become active
        ctx.channel().writeAndFlush(new DiscoverCommand((byte) 0xFF)).sync();
    }
}
