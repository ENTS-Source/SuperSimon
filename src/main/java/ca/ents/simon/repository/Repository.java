package ca.ents.simon.repository;

import ca.ents.simon.entities.Entity;

import java.io.Serializable;
import java.util.Collection;

/**
 * Repository for objects within the project
 *
 * @param <T> the type of entity to represent this repository
 */
public interface Repository<T extends Entity> {

    /**
     * Retrieves a collection of all entities within the repository
     *
     * @return the entities within the repository
     */
    Collection<T> findAll();

    /**
     * Finds an entity by the key provided
     *
     * @param key the key to lookup the object by
     * @return the object, if found. Null if not found.
     */
    T findByKey(Serializable key);

    /**
     * Adds an entity to the repository
     *
     * @param entity the entity to add, cannot be null
     */
    void add(T entity);

    /**
     * Deletes an entity from the repository
     *
     * @param entity the entity to delete, cannot be null
     */
    void delete(T entity);

    /**
     * Saves an entity that has already been added to the repository
     *
     * @param entity the entity to be saved, cannot be null
     */
    void save(T entity);
}
