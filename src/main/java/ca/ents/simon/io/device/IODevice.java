package ca.ents.simon.io.device;

import io.netty.channel.ChannelPipeline;

/**
 * Represents a communication device to issue protocol statements over
 */
public interface IODevice {
    /**
     * Gets the pipeline for this IO device. Will return null if not configured
     *
     * @return the channel pipeline for this device
     */
    ChannelPipeline getPipeline();

    /**
     * Shuts down the IO device
     */
    void shutdown() throws InterruptedException;
}
