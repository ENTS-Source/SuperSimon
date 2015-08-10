package ca.ents.simon.io.session;

import ca.ents.simon.io.command.AddressedSimonCommand;
import ca.ents.simon.io.command.CommandInfo;
import ca.ents.simon.io.command.CommandRegistry;
import ca.ents.simon.io.command.SimonCommand;
import ca.ents.simon.io.device.IODevice;
import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ConcurrentMap;

/**
 * Session manager for dealing with SimonSessions
 */
public class SessionManager {

    private static ConcurrentMap<IODevice, SessionManager> DEVICE_MAP = new ConcurrentHashMap<>();
    private static long TIMEOUT = 500; // milliseconds

    private boolean runNetworking = true;
    private final Object networkLock = new Object();
    private Queue<SimonCommand> inboundCommands = new ConcurrentLinkedQueue<>();
    private Queue<SimonCommand> outboundCommands = new ConcurrentLinkedQueue<>();
    private IODevice device;
    private Map<Byte, SimonSession> sessions = new HashMap<>();

    SessionManager(IODevice device) {
        if (device == null) throw new IllegalArgumentException("IO Device cannot be null");
        this.device = device;
        DEVICE_MAP.put(device, this);

        Channel channel = device.getChannel();
        Thread networkingThread = new Thread(() -> {
            System.out.println("[IO] Waiting for channel to become active...");
            //noinspection StatementWithEmptyBody
            while (!channel.isActive()) ;
            System.out.println("[IO] Channel active!");
            while (runNetworking) {
                while (outboundCommands.peek() != null) {
                    SimonCommand command = outboundCommands.poll();
                    SimonSession session = null;
                    if (command instanceof AddressedSimonCommand)
                        session = createOrFindSession(((AddressedSimonCommand) command).getTargetAddress());

                    System.out.println("[IO] Sending command: " + command.getClass().getName() + " to session: " + session);

                    inboundCommands.clear(); // Clear extra received commands before we send

                    try {
                        ChannelFuture future = channel.writeAndFlush(command).sync();
                        if (!future.isSuccess())
                            future.cause().printStackTrace();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    long sendTime = System.currentTimeMillis();

                    CommandInfo commandInfo = CommandRegistry.getCommandInfo(command.getClass());
                    List<Class<? extends SimonCommand>> responseCommandClasses = commandInfo.getValidResponseClasses();
                    if (responseCommandClasses.size() <= 0) {
                        System.out.println("[IO] No response required");
                        continue;
                    }

                    //noinspection StatementWithEmptyBody
                    while (inboundCommands.peek() == null && System.currentTimeMillis() - sendTime < TIMEOUT) ;

                    if (inboundCommands.peek() == null) {
                        System.out.println("[IO] Session marked as offline: Timeout");
                        if (session != null) session.setOnline(false);
                        continue;
                    }

                    SimonCommand response = inboundCommands.poll();
                    if (responseCommandClasses.contains(response.getClass())) {
                        System.out.println("[IO] Valid response received");
                        // TODO: Event for handling
                    } else {
                        System.out.println("[IO] Session marked as offline: Invalid response");
                        if (session != null) session.setOnline(false);
                    }
                }
                if (runNetworking) {
                    try {
                        synchronized (networkLock) {
                            System.out.println("[IO] Waiting for commands...");
                            networkLock.wait();
                        }
                    } catch (InterruptedException ignored) {
                    }
                }
            }
        });
        networkingThread.start();
    }

    void handleCommand(SimonCommand command) {
        if (command == null) throw new IllegalArgumentException("Command cannot be null");
        inboundCommands.add(command);
        synchronized (networkLock) {
            networkLock.notify();
        }
    }

    void sendCommand(SimonCommand command) {
        if (command == null) throw new IllegalArgumentException("Command cannot be null");
        outboundCommands.add(command);
        synchronized (networkLock) {
            networkLock.notify();
        }
    }

    /**
     * Creates or finds a SimonSession for the given address
     *
     * @param address the address to find or create a session for
     * @return the session for the address
     */
    public SimonSession createOrFindSession(byte address) {
        if (!sessions.containsKey(address))
            sessions.put(address, new SimonSession(address, this));
        return sessions.get(address);
    }

    /**
     * Creates or finds a SessionManager for the given communication device
     *
     * @param device the device to lookup, cannot be null
     * @return the existing SessionManager or a new session manager for the device
     */
    public static SessionManager forDevice(IODevice device) {
        if (device == null) throw new IllegalArgumentException("Communication device is required");
        if (!DEVICE_MAP.containsKey(device))
            DEVICE_MAP.put(device, new SessionManager(device));
        return DEVICE_MAP.get(device);
    }

    /**
     * Shuts down the session manager
     */
    public void shutdown() {
        runNetworking = false;
        synchronized (networkLock) {
            networkLock.notify();
        }
        try {
            device.shutdown();
        } catch (InterruptedException ignored) {
        }
    }
}
