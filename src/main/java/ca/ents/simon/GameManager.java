package ca.ents.simon;

import ca.ents.simon.configuration.ConfigKey;
import ca.ents.simon.configuration.SimonConfiguration;
import ca.ents.simon.io.device.IODevice;
import ca.ents.simon.io.device.SerialPort;
import ca.ents.simon.io.session.SessionManager;
import ca.ents.simon.repository.ScoreRepository;
import ca.ents.simon.util.EntsImage;
import ca.ents.simon.util.UIGroup;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Text;

/**
 * Game operation for Simon
 */
public class GameManager {

    private static final String ID_TOTAL_PLAYERS_LABEL = "totalPlayersLabel";
    private static final String ID_TOTAL_PLAYERS_COUNT = "totalPlayersCount";
    private static final String ID_DIVIDER = "divider";
    private static final String ID_HEADER_GAME_NAME = "gameName";

    private static final int TOP_PLAYER_COUNT = 5;

    private byte playerAddrStart = SimonConfiguration.getByteValue(ConfigKey.GAME_ADDRESSING_START);
    private byte playerAddrEnd = SimonConfiguration.getByteValue(ConfigKey.GAME_ADDRESSING_END);
    private UIGroup ui;
    private Scene scene;
    private SessionManager sessionManager;
    private ScoreRepository scoreRepo;

    public GameManager() {
        scoreRepo = new ScoreRepository();
    }

    public void configureScene(Scene scene, Group root) {
        ui = new UIGroup(root);
        this.scene = scene;
        loadStylesheets(scene);
        scene.widthProperty().addListener((observable, oldValue, newValue) -> updatePositioning());
        scene.heightProperty().addListener((observable, oldValue, newValue) -> updatePositioning());

        // Header
        Image logoImage = EntsImage.LOGO.original();
        ImageView logo = new ImageView(logoImage);
        logo.setX(10);
        logo.setY(10);
        ui.addChild(logo);

        Text headerText = new Text("ENTS SuperSimon");
        headerText.setX(logoImage.getWidth() + 30);
        headerText.setY(logoImage.getHeight() - 20);
        headerText.setId(ID_HEADER_GAME_NAME);
        ui.addChild(headerText);

        // Show total players
        Text totalPlayersLabel = new Text("Total players:");
        totalPlayersLabel.setId(ID_TOTAL_PLAYERS_LABEL);
        ui.addChild(totalPlayersLabel);

        Text totalPlayersCount = new Text("0");
        totalPlayersCount.setId(ID_TOTAL_PLAYERS_COUNT);
        ui.addChild(totalPlayersCount);

        // Add sidebar
        double headerHeight = logoImage.getHeight() + 25;
        double playAreaHeight = scene.getHeight() - headerHeight;
        Rectangle divider = new Rectangle(scene.getWidth() - 350, headerHeight, 5, playAreaHeight - headerHeight);
        divider.setId(ID_DIVIDER);
        ui.addChild(divider);

        // Add player area
        // TODO

        updatePositioning();
    }

    public void beginOperation() {
        String deviceName = SimonConfiguration.getValue(ConfigKey.IO_DEVICE_SERIALPORT_PORTNAME);
        IODevice device;
        if (deviceName == null || deviceName.equalsIgnoreCase("discover"))
            device = new SerialPort();
        else device = new SerialPort(deviceName);
        sessionManager = SessionManager.forDevice(device);

        discoverPlayers();
    }

    public void shutdown() {
        sessionManager.shutdown();
    }

    private void updatePositioning() {
        updateTotalPlayers();
        updatePlayers();
        updateSidebar();
    }

    private void updateTotalPlayers() {
        Text lblCount = (Text) ui.findById(ID_TOTAL_PLAYERS_COUNT);
        Text lblText = (Text) ui.findById(ID_TOTAL_PLAYERS_LABEL);

        lblCount.setText(scoreRepo.findAll().size() + "");
        lblCount.setX(scene.getWidth() - lblCount.getBoundsInParent().getWidth() - 25);
        lblCount.setY(lblCount.getBoundsInParent().getHeight());

        lblText.setX(lblCount.getX() - lblText.getBoundsInParent().getWidth() - 10);
        lblText.setY(lblCount.getY());
    }

    private void updatePlayers() {

    }

    private void updateSidebar() {
        Rectangle divider = (Rectangle) ui.findById(ID_DIVIDER);
        divider.setX(scene.getWidth() - 350);
    }

    private void discoverPlayers() {
        for (byte address = playerAddrStart; address <= playerAddrEnd; address++) {
            sessionManager.createOrFindSession(address).tryDiscover();
        }
    }

    private void loadStylesheets(Scene scene) {
        scene.getStylesheets().add(getClass().getResource("/styles/main.css").toExternalForm());
    }
}
