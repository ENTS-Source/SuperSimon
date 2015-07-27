package ca.ents.simon.util;

import javafx.scene.text.Font;

/**
 * Represents a font for ENTS JavaFX projects
 *
 * @author TravisR
 */
public class EntsFont {

    public static final EntsFont CONDENSED_ITALIC = new EntsFont(EntsFont.class.getResource("/fonts/LeagueGothic-CondensedItalic.otf").toExternalForm());
    public static final EntsFont CONDENSED_REGULAR = new EntsFont(EntsFont.class.getResource("/fonts/LeagueGothic-CondensedRegular.otf").toExternalForm());
    public static final EntsFont ITALIC = new EntsFont(EntsFont.class.getResource("/fonts/LeagueGothic-Italic.otf").toExternalForm());
    public static final EntsFont REGULAR = new EntsFont(EntsFont.class.getResource("/fonts/LeagueGothic-Regular.otf").toExternalForm());

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

}
