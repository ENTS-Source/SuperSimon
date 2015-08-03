package ca.ents.simon.entities;

/**
 * Represents a storage entity
 */
public interface Entity {
    /**
     * Used to identify methods that should not be deleted or used within the application because
     * they are intended for use only by the ORM.
     */
    @interface ForOrm {
    }
}
