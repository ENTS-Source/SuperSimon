package ca.ents.simon.io.device;

import io.netty.channel.Channel;

/**
 * Represents a communication device to issue protocol statements over
 */
public interface IODevice {
    /**
     * Gets the channel this IO device exposes
     *
     * @return the channel for this IO device
     */
    Channel getChannel();

    /**
     * Shuts down the IO device
     */
    void shutdown() throws InterruptedException;
}
