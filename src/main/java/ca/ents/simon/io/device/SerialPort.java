package ca.ents.simon.io.device;

import ca.ents.simon.io.decoder.SimonDecoder;
import ca.ents.simon.io.decoder.SimonEncoder;
import ca.ents.simon.io.decoder.SimonFrameDecoder;
import com.beauhinks.purejavacomm.PureJavaCommChannel;
import com.beauhinks.purejavacomm.PureJavaCommDeviceAddress;
import io.netty.bootstrap.Bootstrap;
import io.netty.channel.*;
import io.netty.channel.oio.OioEventLoopGroup;
import io.netty.handler.codec.LineBasedFrameDecoder;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;
import purejavacomm.CommPortIdentifier;

import java.util.Enumeration;

/**
 * Serial port transport
 */
public class SerialPort implements IODevice {

    private Channel channel;
    private EventLoopGroup group;

    /**
     * Creates a new serial port device that runs an auto-discover sequence until
     * a port is found. If a serial port cannot be found then an exception is thrown.
     */
    public SerialPort() {
        CommPortIdentifier port;
        Enumeration e = CommPortIdentifier.getPortIdentifiers();
        while (e.hasMoreElements()) {
            port = (CommPortIdentifier) e.nextElement();
            System.out.println("Attempting connection on port " + port.getName());
            if (tryInit(port.getName())) {
                init(port.getName());
                return;
            }
        }

        throw new IllegalStateException("Failed to initialize serial port: Could not find a responsive serial port.");
    }

    /**
     * "
     * Creates a new serial port device that attaches to the given name. If the port
     * cannot be opened then an exception is thrown.
     *
     * @param portName the port name to open
     */
    public SerialPort(String portName) {
        init(portName);
    }

    private boolean tryInit(String portName) {
        EventLoopGroup group = new OioEventLoopGroup();
        try {
            DiscoverPortHandler portHandler = new DiscoverPortHandler();
            Bootstrap b = new Bootstrap();
            b.group(group)
                    .channel(PureJavaCommChannel.class)
                    .handler(new ChannelInitializer<PureJavaCommChannel>() {
                        @Override
                        public void initChannel(PureJavaCommChannel ch) throws Exception {
                            ch.pipeline().addLast(
                                    new LineBasedFrameDecoder(32768),
                                    new StringEncoder(),
                                    new StringDecoder(),
                                    portHandler
                            );
                        }
                    });

            b.connect(new PureJavaCommDeviceAddress(portName)).sync();
            //noinspection StatementWithEmptyBody
            while (portHandler.isPendingResponse()) {
                // Wait
                Thread.sleep(1); // So that we can exit this loop at some point
            }
            System.out.println("Device alive? " + portHandler.isActive());
            return portHandler.isActive();
        } catch (InterruptedException e) {
            return false;
        } finally {
            group.shutdownGracefully();
        }
    }

    private void init(String portName) {
        if (portName == null) throw new IllegalArgumentException("Port name cannot be null");

        group = new OioEventLoopGroup();
        Bootstrap b = new Bootstrap();
        b.group(group).channel(PureJavaCommChannel.class).handler(new ChannelInitializer<PureJavaCommChannel>() {
            @Override
            protected void initChannel(PureJavaCommChannel ch) throws Exception {
                ch.pipeline().addLast(
                        new SimonFrameDecoder(),
                        new SimonEncoder(),
                        new SimonDecoder()
                );
            }
        });
        try {
            channel = b.connect(new PureJavaCommDeviceAddress(portName)).sync().channel();
        } catch (InterruptedException e) {
            throw new RuntimeException("Could not contact serial port", e);
        }
    }

    @Override
    public Channel getChannel() {
        return channel;
    }

    @Override
    public void shutdown() throws InterruptedException {
        group.shutdownGracefully().sync();
    }

    private class DiscoverPortHandler extends SimpleChannelInboundHandler<String> {

        private final int[] DETECT_COMMAND = {0xD, 0xE, 0xA, 0xD, 0xC, 0x0, 0xD, 0xE};

        private boolean responded = false;
        private boolean okResponse = false;
        private long sendTime = 0;

        private String getCommand() {
            String command = "";
            for (int i : DETECT_COMMAND)
                command += (char) i;
            return command;
        }

        @Override
        public void channelActive(ChannelHandlerContext ctx) throws Exception {
            sendTime = System.currentTimeMillis();
            ctx.writeAndFlush(getCommand());
        }

        @Override
        protected void channelRead0(ChannelHandlerContext channelHandlerContext, String s) throws Exception {
            responded = true;
            if (s.equals("HELLOWORLD")) {
                okResponse = true;
            }
            channelHandlerContext.close();
        }

        public boolean isActive() {
            return !isPendingResponse() && okResponse;
        }

        public boolean isPendingResponse() {
            boolean timedOut = sendTime > 0 && System.currentTimeMillis() - sendTime > 500;
            return !responded && !timedOut;
        }
    }

}
