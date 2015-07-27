package ca.ents.simon;

import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.effect.BoxBlur;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.StrokeType;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.lang.Math.random;

public class App extends Application{

    @Override
    public void start(Stage primaryStage) throws Exception {
        Group root = new Group();
        Scene scene = new Scene(root, 800, 600, Color.BLACK);
        primaryStage.setScene(scene);

        final Map<String, double[]> velocities = new HashMap<>();
        Group circles = new Group();
        List<Circle> circleList = new ArrayList<>();
        for (int i = 0; i < 1; i++) {
            Color color = Color.color(random(), random(), random(), 0.16);
            Circle circle = new Circle(15, color);
            circle.setStrokeType(StrokeType.OUTSIDE);
            circle.setStroke(Color.color(color.getRed(), color.getGreen(), color.getBlue(), 0.32));
            circle.setStrokeWidth(4);
            circles.getChildren().add(circle);
            circleList.add(circle);
            circle.setId("circle" + i);
            velocities.put("circle" + i, new double[]{random() * (random() * 5), random() * (random() * 5)});
        }

        for (Map.Entry<String, double[]> velocity : velocities.entrySet()) {
            double offset = 0.4;
            velocity.getValue()[0] += offset;
            velocity.getValue()[1] += offset;
        }

        circles.setEffect(new BoxBlur(5, 5, 1));

        final Group particles = new Group();
        root.getChildren().add(particles);

        root.getChildren().add(circles);

        // Move to somewhere on screen
        for (Circle circle : circleList) {
            double doubleOffset = circle.getRadius() * 2;

            double maxWidth = scene.getWidth() - doubleOffset;
            double maxHeight = scene.getHeight() - doubleOffset;

            double x = (random() * maxWidth) + (doubleOffset / 2);
            double y = (random() * maxHeight) + (doubleOffset / 2);

            circle.setTranslateX(x);
            circle.setTranslateY(y);
        }


        new AnimationTimer() {
            @Override
            public void handle(long now) {
                for (Circle circle : circleList) {
                    double[] velocity = velocities.get(circle.getId());

                    double lastX = circle.getTranslateX();
                    double lastY = circle.getTranslateY();

                    double ivx = -velocity[0];
                    double ivy = -velocity[1];
                    for (int i = 0; i < 2; i++) {
                        for (int j = 0; j < 2; j++) {
                            boolean xFloat = i == 0;
                            boolean yFloat = j == 0;

                            int[] options = new int[]{1, 3, 5};
                            for (int o : options) {
                                double vx = ivx + random();
                                double vy = ivy + random();
                                double px = lastX + (xFloat ? o : -o) + (random() * (o * (xFloat ? -1 : 1)));
                                double py = lastY + (yFloat ? o : -o) + (random() * (o * (yFloat ? -1 : 1)));
                                particles.getChildren().add(new Particle((Color) circle.getFill(), px, py, 1, 250, vx, vy));
                            }
                        }
                    }

                    double x = circle.getTranslateX() + velocity[0];
                    double y = circle.getTranslateY() + velocity[1];

                    double rx = x + circle.getRadius();
                    double lx = x - circle.getRadius();
                    double ty = y - circle.getRadius();
                    double by = y + circle.getRadius();

                    // Bounce
                    if (lx <= 0 || rx >= scene.getWidth())
                        velocity[0] = -velocity[0];
                    if (ty <= 0 || by >= scene.getHeight())
                        velocity[1] = -velocity[1];

                    circle.setTranslateX(x);
                    circle.setTranslateY(y);
                }

                List<Node> remove = new ArrayList<>();
                for (Node node : particles.getChildren()) {
                    Particle particle = (Particle) node;
                    particle.moveAndFade(scene);

                    if (particle.isFaded())
                        remove.add(particle);
                }

                particles.getChildren().removeAll(remove);
            }
        }.start();


        Circle playerCircle = new Circle(0, 0, 25);
        playerCircle.setFill(Color.DARKGREEN);

        scene.setOnMouseMoved(event -> {
            playerCircle.setCenterX(event.getSceneX());
            playerCircle.setCenterY(event.getSceneY());
        });

        root.getChildren().add(playerCircle);

        primaryStage.show();
    }


    public static void main(String[] args) {
        launch(args);
    }
}
