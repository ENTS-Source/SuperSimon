package ca.ents.simon.util;

import javafx.scene.image.Image;

/**
 * Represents an image that can be defined as a particular size
 */
public class EntsImage {

    public static final EntsImage LOGO = new EntsImage(getResource("/images/logo.png"));

    private String path;

    private EntsImage(String path) {
        if (path == null) throw new IllegalArgumentException("Image path cannot be null");
        this.path = path;
    }

    /**
     * Creates a new JavaFX image for the given ENTS image without resizing
     *
     * @return the JavaFX image
     */
    public Image original() {
        return new Image(path);
    }

    // Parameter javadocs for size(...) copied from JavaFX
    // https://docs.oracle.com/javafx/2/api/javafx/scene/image/Image.html#Image(java.lang.String, double, double, boolean, boolean)

    /**
     * Creates a new JavaFX image for the given ENTS image that preserves scaling and uses a smooth algorithm
     *
     * @param width  the image's bounding box width
     * @param height the image's bounding box height
     * @return the JavaFX image
     */
    public Image size(double width, double height) {
        return size(width, height, true, true);
    }

    /**
     * Creates a new JavaFX image for the given ENTS image
     *
     * @param width         the image's bounding box width
     * @param height        the image's bounding box height
     * @param preserveRatio indicates whether to preserve the aspect ratio of the original image when scaling to fit the image within the specified bounding box
     * @param smooth        indicates whether to use a better quality filtering algorithm or a faster one when scaling this image to fit within the specified bounding box
     * @return the JavaFX image
     */
    public Image size(double width, double height, boolean preserveRatio, boolean smooth) {
        return new Image(path, width, height, preserveRatio, smooth);
    }

    private static String getResource(String name) {
        return EntsImage.class.getResource(name).toExternalForm();
    }
}
