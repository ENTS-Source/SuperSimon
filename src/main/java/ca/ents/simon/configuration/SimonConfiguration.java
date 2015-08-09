package ca.ents.simon.configuration;

import java.io.*;
import java.util.Objects;
import java.util.Properties;

/**
 * Configuration for SuperSimon
 */
public final class SimonConfiguration {

    private static Properties settings;

    static {
        try {
            File targetFile = new File("..", "simon.properties");
            if (!targetFile.exists())
                copyTemplateConfiguration(targetFile);
            addMissingProperties(targetFile);
            settings = new Properties();
            settings.load(new FileInputStream(targetFile));
        } catch (IOException e) {
            throw new RuntimeException("Could not load configuration", e);
        }
    }

    private SimonConfiguration() {
    }

    private static void copyTemplateConfiguration(File targetFile) throws IOException {
        OutputStreamWriter writer = new OutputStreamWriter(new FileOutputStream(targetFile));
        InputStreamReader reader = new InputStreamReader(SimonConfiguration.class.getResourceAsStream("/default.properties"));
        int bite;
        while ((bite = reader.read()) != -1)
            writer.write(bite);
        writer.close();
        reader.close();
    }

    private static void addMissingProperties(File targetConfiguration) throws IOException {
        Properties fromFile = new Properties();
        fromFile.load(SimonConfiguration.class.getResourceAsStream("/default.properties"));
        fromFile.load(new FileInputStream(targetConfiguration));
        fromFile.store(new FileOutputStream(targetConfiguration), "ENTS SuperSimon Configuration");
    }

    /**
     * Gets the raw String value for a given configuration key, returning null if the key is not found
     *
     * @param key the key to lookup, should not be null
     * @return the String value of the key, or null if not found
     */
    public static String getValue(ConfigKey key) {
        Object value = settings.get(key.getSystemName());
        if (value == null) return null;
        return value.toString();
    }

    /**
     * Gets the interpreted boolean value for the given configuration key, returning false if the key is not
     * found.
     *
     * @param key the key to lookup, should not be null
     * @return the interpreted boolean value of the key, or null if not found
     */
    public static boolean getBooleanValue(ConfigKey key) {
        return Objects.equals(getValue(key), "true");
    }

    /**
     * Gets the byte value for a given configuration key, returning 0 if the key is not found
     *
     * @param key the key to lookup, should not be null
     * @return the byte value of the key, or null if not found
     */
    public static byte getByteValue(ConfigKey key) {
        String value = getValue(key);
        if (value == null) return 0;
        return Byte.valueOf(value);
    }
}
