package ca.ents.simon;

import ca.ents.simon.util.EntsFont;
import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.input.KeyCode;
import javafx.scene.text.Text;
import javafx.stage.Stage;

/**
 * Main entry point for the application
 *
 * @author TravisR
 */
public class App extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception {
        Group root = new Group();

        double minWidth = 1920;
        double minHeight = 1280;

        Scene scene = new Scene(root, minWidth, minHeight, Branding.BACKGROUND_COLOR);
        primaryStage.setScene(scene);

        // TODO: UI Code
        Text text = new Text("Test Text");
        text.setFont(EntsFont.REGULAR.size(20));
        text.setX(100);
        text.setY(100);
        root.getChildren().add(text);

        primaryStage.setMaximized(true);
        primaryStage.setMinWidth(minWidth);
        primaryStage.setMinHeight(minHeight);
        primaryStage.setResizable(true);
        primaryStage.setTitle(Branding.GAME_NAME);
        primaryStage.setFullScreen(false); // TODO: Configurable
        primaryStage.setFullScreenExitHint(""); // Hides the message all together
        scene.setOnKeyPressed(event -> {
            if (event.getCode() == KeyCode.ESCAPE)
                primaryStage.close();
        });
        primaryStage.show();
    }


    public static void main(String[] args) {
        launch(args);
    }
}
