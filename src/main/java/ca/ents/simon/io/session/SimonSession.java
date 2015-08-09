package ca.ents.simon.io.session;

import ca.ents.simon.io.command.CommandInfo;
import ca.ents.simon.io.command.CommandRegistry;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.command.impl.DiscoverCommand;
import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;

import java.util.List;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * A session on the communication device
 */
public class SimonSession {

    private static long TIMEOUT = 2500; // milliseconds

    private byte address;
    private boolean validSession = false;
    private final Object lockObject = new Object();

    private Queue<SimonCommand> inboundCommands = new ConcurrentLinkedQueue<>();
    private Queue<SimonCommand> outboundCommands = new ConcurrentLinkedQueue<>();

    SimonSession(byte address, Channel channel) {
        if (channel == null) throw new IllegalArgumentException("Channel cannot be null for a session");
        this.address = address;

        Thread networkingThread = new Thread(() -> {
            //noinspection StatementWithEmptyBody
            while (!channel.isActive()) ;
            while (outboundCommands.peek() != null) {
                SimonCommand command = outboundCommands.poll();
                System.out.println("Sending command to player " + address + ": " + command.getClass().getName());

                inboundCommands.clear(); // Clear extra received commands before we send

                try {
                    ChannelFuture future = channel.writeAndFlush(command).sync();
                    if (!future.isSuccess())
                        //noinspection ThrowableResultOfMethodCallIgnored
                        future.cause().printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                long sendTime = System.currentTimeMillis();

                CommandInfo commandInfo = CommandRegistry.getCommandInfo(command.getClass());
                List<Class<? extends SimonCommand>> responseCommandClasses = commandInfo.getValidResponseClasses();
                if (responseCommandClasses.size() <= 0) {
                    System.out.println("No response required by player " + address);
                    continue;
                }

                //noinspection StatementWithEmptyBody
                while (inboundCommands.peek() == null && System.currentTimeMillis() - sendTime < TIMEOUT) ;

                if (inboundCommands.peek() == null) {
                    System.out.println("Player " + address + " kicked offline: Timeout");
                    validSession = false;
                    // TODO: Player offline event
                    continue;
                }

                SimonCommand response = inboundCommands.poll();
                System.out.println("Got response from player " + address + ": " + response);
                if (responseCommandClasses.contains(response.getClass())) {
                    System.out.println("Valid response by player " + address);
                    // TODO: Event for handling
                } else {
                    System.out.println("Player " + address + " kicked offline: Invalid response to command '" + command.getClass().getName() + "'");
                    validSession = false;
                    // TODO: Player offline event
                }
            }
            try {
                synchronized (lockObject) {
                    lockObject.wait();
                }
            } catch (InterruptedException ignored) {
            }
        });
        networkingThread.start();
    }

    /**
     * Gets the address of this session
     *
     * @return the session address
     */
    public byte getAddress() {
        return address;
    }

    /**
     * Processes a SimonCommand for handling. May not be processed immediately. This is non-blocking.
     *
     * @param command the command to process, cannot be null
     */
    public void handleCommand(SimonCommand command) {
        if (command == null) throw new IllegalArgumentException("Command to handle cannot be null");
        inboundCommands.add(command);
        synchronized (lockObject) {
            lockObject.notify();
        }
    }

    /**
     * Sends a command to this session
     *
     * @param command the command to send to the session, cannot be null
     */
    public void sendCommand(SimonCommand command) {
        if (command == null) throw new IllegalArgumentException("Command to send cannot be null");
        outboundCommands.add(command);
        synchronized (lockObject) {
            lockObject.notify();
        }
    }

    /**
     * Attempts a discovery on this session
     */
    public void tryDiscover() {
        sendCommand(new DiscoverCommand(address));
    }

}
