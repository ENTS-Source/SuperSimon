package ca.ents.simon;

import ca.ents.simon.io.session.SessionManager;
import ca.ents.simon.io.device.IODevice;
import ca.ents.simon.io.device.SerialPort;
import ca.ents.simon.io.session.SimonSession;
import ca.ents.simon.util.EntsFont;
import ca.ents.simon.util.EntsImage;
import ca.ents.simon.util.UIGroup;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.text.Text;

/**
 * Game operation for Simon
 */
public class GameManager {

    private static final String ID_TOTAL_PLAYERS_LABEL = "totalPlayersLabel";
    private static final String ID_TOTAL_PLAYERS_COUNT = "totalPlayersCount";

    private UIGroup ui;

    public void configureScene(Scene scene, Group root) {
        ui = new UIGroup(root);

        // Header
        Image logoImage = EntsImage.LOGO.original();
        ImageView logo = new ImageView(logoImage);
        logo.setX(10);
        logo.setY(10);
        ui.addChild(logo);

        Text headerText = new Text(Branding.GAME_NAME);
        headerText.setFont(EntsFont.REGULAR.size(144));
        headerText.setX(logoImage.getWidth() + 30);
        headerText.setY(logoImage.getHeight() - 20);
        ui.addChild(headerText);

        // Show total players
        Text totalPlayersLabel = new Text("Total players:");
        totalPlayersLabel.setFont(EntsFont.REGULAR.size(25));
        totalPlayersLabel.setFill(Branding.MUTED_TEXT_COLOR);
        totalPlayersLabel.setId(ID_TOTAL_PLAYERS_LABEL);
        ui.addChild(totalPlayersLabel);

        Text totalPlayersCount = new Text("0");
        totalPlayersCount.setFont(EntsFont.REGULAR.size(25));
        totalPlayersCount.setFill(Branding.MUTED_TEXT_COLOR);
        totalPlayersCount.setId(ID_TOTAL_PLAYERS_COUNT);
        ui.addChild(totalPlayersCount);

        updateTotalPlayers();
    }

    public void beginOperation() {
        // TODO

        IODevice device = new SerialPort("COM8");
        SessionManager sessions = SessionManager.forDevice(device);
        SimonSession session = sessions.createOrFindSession((byte) 0x03);
        session.tryDiscover();
    }

    public void shutdown() {
        // TODO
    }

    private void updateTotalPlayers() {
        // TODO
    }
}
