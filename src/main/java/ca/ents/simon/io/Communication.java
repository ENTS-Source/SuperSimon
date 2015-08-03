package ca.ents.simon.io;

import ca.ents.simon.io.device.IODevice;

/**
 * Central communication platform for communication between players
 */
public class Communication { // TODO: Better name?

    private IODevice device;

    public Communication(IODevice device) {
        if (device == null) throw new IllegalArgumentException("IO Device cannot be null");
        this.device = device;
    }

}
