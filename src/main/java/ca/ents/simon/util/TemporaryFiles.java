package ca.ents.simon.util;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Temporary file manager for the application
 */
public class TemporaryFiles {

    private static Map<TempFile, File> HANDLES = new HashMap<>();

    private TemporaryFiles() {
    }

    /**
     * Retrieves a temporary file
     *
     * @param tempFile the temporary file to load
     * @return the path to the file
     */
    public static File get(TempFile tempFile) {
        if (!HANDLES.containsKey(tempFile)) {
            HANDLES.put(tempFile, retrieveFile(tempFile.internalPath));
        }
        return HANDLES.get(tempFile);
    }

    @SuppressWarnings("ResultOfMethodCallIgnored")
    private static File retrieveFile(String internalPath) {
        try {
            File destination = new File("temp", UUID.randomUUID().toString() + ".tmp");
            destination.getParentFile().mkdirs();

            InputStream in = TemporaryFiles.class.getResourceAsStream(internalPath);
            FileOutputStream out = new FileOutputStream(destination, false);
            byte[] buffer = new byte[2048];
            int len;
            while ((len = in.read(buffer)) > 0)
                out.write(buffer, 0, len);
            out.close();
            in.close();

            return destination;
        } catch (IOException e) {
            throw new RuntimeException("Could not store temporary file: " + internalPath, e);
        }
    }

    public enum TempFile {
        ;

        private final String internalPath;

        TempFile(String internalPath) {
            this.internalPath = internalPath;
        }
    }

}
