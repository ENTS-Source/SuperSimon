package ca.ents.simon;

import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;

public class Particle extends Circle {

    private long fadeTime = 0;
    private long startFade = 0;
    private double[] velocity;

    public Particle(Color color, double x, double y, double size, long fadeTime, double xVelocity, double yVelocity) {
        super(x, y, size, color);

        //super.setEffect(new GaussianBlur(size / 2));

        this.fadeTime = fadeTime;
        this.velocity = new double[]{xVelocity, yVelocity};
        this.startFade = System.currentTimeMillis();
    }

    public void moveAndFade(Scene bounds) {
        double x = getCenterX() + velocity[0];
        double y = getCenterY() + velocity[1];

        if (x - getRadius() <= 0 || x + getRadius() >= bounds.getWidth())
            velocity[0] = -velocity[0];
        if (y - getRadius() <= 0 || y + getRadius() >= bounds.getHeight())
            velocity[1] = -velocity[1];

        setCenterX(x);
        setCenterY(y);

        long timeSinceStart = System.currentTimeMillis() - startFade;

        double opacity = 1 - ((double) timeSinceStart / fadeTime);
        opacity = Math.min(0.25, Math.max(0, opacity));
        Color fill = (Color) getFill();
        setFill(Color.color(fill.getRed(), fill.getGreen(), fill.getBlue(), opacity));
    }

    public boolean isFaded() {
        return ((Color) getFill()).getOpacity() <= 0;
    }

}
