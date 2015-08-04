package ca.ents.simon.configuration;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

/**
 * Configuration for SuperSimon
 */
public final class Configuration {

    private static Properties settings;

    static {
        File targetFile = new File("..", "simon.properties");
        if (!targetFile.exists())
            copyTemplateConfiguration();
        addMissingProperties(targetFile);
        settings = new Properties();
        try {
            settings.load(new FileInputStream(targetFile));
        } catch (IOException e) {
            throw new RuntimeException("Could not load configuration", e);
        }
    }

    private Configuration() {
    }

    private static void copyTemplateConfiguration() {
        // TODO: Actually copy configuration
    }

    private static void addMissingProperties(File targetConfiguration) {
        // TODO: Actually ensure properties are added
    }

    // TODO: Document
    // TODO: Provide default
    // TODO: getInt, getBool, etc...
    public String getValue(ConfigKey key) {
        Object value = settings.get(key);
        if (value == null) return null;
        return value.toString();
    }

}
