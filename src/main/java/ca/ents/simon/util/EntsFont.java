package ca.ents.simon.util;

import javafx.scene.text.Font;

/**
 * Represents a font for ENTS JavaFX projects
 */
public class EntsFont {

    public static final EntsFont CONDENSED_ITALIC = new EntsFont(getResource("/fonts/LeagueGothic-CondensedItalic.otf"));
    public static final EntsFont CONDENSED_REGULAR = new EntsFont(getResource("/fonts/LeagueGothic-CondensedRegular.otf"));
    public static final EntsFont ITALIC = new EntsFont(getResource("/fonts/LeagueGothic-Italic.otf"));
    public static final EntsFont REGULAR = new EntsFont(getResource("/fonts/LeagueGothic-Regular.otf"));

    private String path;

    private EntsFont(String otfPath) {
        if (otfPath == null) throw new IllegalArgumentException("otfPath cannot be null");
        path = otfPath;
    }

    /**
     * Gets a font of the size specified for the OTF path specified
     *
     * @param size the size of font to use
     * @return the font generated
     */
    public Font size(double size) {
        return Font.loadFont(path, size);
    }

    private static String getResource(String name) {
        return EntsFont.class.getResource(name).toExternalForm();
    }
}
