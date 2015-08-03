package ca.ents.simon.entities;

/**
 * Represents a player score
 */
public final class Score implements Entity {

    private int id;
    private long score;
    private int playerNumber;

    @ForOrm
    private Score() {
    }

    public Score(int playerNumber, long totalScore) {
        score = totalScore;
        this.playerNumber = playerNumber;
    }

    @ForOrm
    private void setId(int id) {
        this.id = id;
    }

    @ForOrm
    private void setScore(long score) {
        this.score = score;
    }

    @ForOrm
    private void setPlayerNumber(int playerNumber) {
        this.playerNumber = playerNumber;
    }

    @ForOrm
    private int getId() {
        return id;
    }

    public long getScore() {
        return score;
    }

    public int getPlayerNumber() {
        return playerNumber;
    }
}
