package ca.ents.simon.repository.concrete;

import ca.ents.simon.entities.Score;

public class ScoreRepository extends Repository<Score> implements ca.ents.simon.repository.ScoreRepository {
    public ScoreRepository() {
        super(Score.class);
    }
}
