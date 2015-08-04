package ca.ents.simon.configuration;

/**
 * Configuration keys available within the configuration
 */
public enum ConfigKey {
    /**
     * boolean - Whether or not the UI should be in fullscreen mode
     */
    UI_FULLSCREEN("ui.fullscreen"),
    /**
     * int - The minimum width for the UI (only applies for non-fullscreen operation)
     */
    UI_MIN_WIDTH("ui.minWidth"),
    /**
     * int - The minimum height for the UI (only applies for non-fullscreen operation)
     */
    UI_MIN_HEIGHT("ui.minHeight"),
    /**
     * String - The class name of the IODevice to be used
     *
     * @see ca.ents.simon.io.device.IODevice
     */
    IO_DEVICE_CLASS("io.device"),
    /**
     * String - The serial port name to be used. Only applies if the {@link ca.ents.simon.configuration.ConfigKey#IO_DEVICE_CLASS}
     * is a {@link ca.ents.simon.io.device.SerialPort}. May be "discover" to indicate that the system should attempt to find an
     * appropriate serial port to be used.
     *
     * @see ca.ents.simon.io.device.SerialPort
     */
    IO_DEVICE_SERIALPORT_PORTNAME("io.device.SerialPort.portName"),
    /**
     * int - The address to start the player search at (inclusive)
     */
    GAME_ADDRESSING_START("game.addresses.start"),
    /**
     * int - The address to end the player search at (inclusive)
     */
    GAME_ADDRESSING_END("game.addresses.end");


    private String systemName;

    ConfigKey(String sysName) {
        this.systemName = sysName;
    }

    String getSystemName() {
        return systemName;
    }

}
