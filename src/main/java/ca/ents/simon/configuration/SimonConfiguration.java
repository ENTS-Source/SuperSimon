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

    // TODO: Allow default values
    // TODO: Other getValue methods (int, double, etc)

    public static String getValue(ConfigKey key) {
        Object value = settings.get(key);
        if (value == null) return null;
        return value.toString();
    }

    public static boolean getBooleanValue(ConfigKey key) {
        return Objects.equals(getValue(key), "true");
    }

}
