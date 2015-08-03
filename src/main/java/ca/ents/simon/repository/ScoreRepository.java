package ca.ents.simon.repository;

import ca.ents.simon.entities.Score;

public class ScoreRepository extends Repository<Score> {
    public ScoreRepository() {
        super(Score.class);
    }
}
