package ca.ents.simon.repository;


import ca.ents.simon.configuration.ConfigKey;
import ca.ents.simon.configuration.SimonConfiguration;
import ca.ents.simon.entities.Entity;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;
import org.reflections.Reflections;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * Repository for entities within the project
 *
 * @param <T> the type of entity to be provided by this repository
 */
public abstract class Repository<T extends Entity> {

    private final static SessionFactory SESSION_FACTORY;
    private Session currentSession;
    private Class<T> supportingClass;

    static {
        Configuration hibernateConf = new Configuration();

        // General properties
        String dbHost = SimonConfiguration.getValue(ConfigKey.MYSQL_HOSTNAME);
        String dbPort = SimonConfiguration.getValue(ConfigKey.MYSQL_PORT);
        String dbDatabase = SimonConfiguration.getValue(ConfigKey.MYSQL_DATABASE);
        String dbUsername = SimonConfiguration.getValue(ConfigKey.MYSQL_USERNAME);
        String dbPassword = SimonConfiguration.getValue(ConfigKey.MYSQL_PASSWORD);
        hibernateConf.setProperty("hibernate.connection.provider_class", "com.zaxxer.hikari.hibernate.HikariConnectionProvider");
        hibernateConf.setProperty("hibernate.hikari.dataSourceClassName", "com.mysql.jdbc.jdbc2.optional.MysqlDataSource");
        hibernateConf.setProperty("hibernate.hikari.dataSource.url", "jdbc:mysql://" + dbHost + ":" + dbPort + "/" + dbDatabase);
        hibernateConf.setProperty("hibernate.hikari.dataSource.user", dbUsername);
        hibernateConf.setProperty("hibernate.hikari.dataSource.password", dbPassword);
        hibernateConf.setProperty("hibernate.hikari.dataSource.cachePrepStmts", "true");
        hibernateConf.setProperty("hibernate.hikari.dataSource.prepStmtCacheSize", "250");
        hibernateConf.setProperty("hibernate.hikari.dataSource.prepStmtCacheSqlLimit", "2048");

        // Setup mappings
        Reflections reflections = new Reflections(Entity.class.getPackage().getName());
        reflections.getSubTypesOf(Entity.class).forEach(hibernateConf::addClass);

        // Configure session factory
        ServiceRegistry serviceRegistry = new StandardServiceRegistryBuilder().applySettings(hibernateConf.getProperties()).build();
        SESSION_FACTORY = hibernateConf.buildSessionFactory(serviceRegistry);

        // Create database structure
        try (Session seedSession = SESSION_FACTORY.openSession()) {
            seedSession.createSQLQuery(readInitScript()).executeUpdate();
        } catch (IOException e) {
            throw new RuntimeException("Could not initialize database", e);
        }
    }

    protected Repository(Class<T> supportingClass) {
        currentSession = SESSION_FACTORY.openSession();
        this.supportingClass = supportingClass;
    }

    /**
     * Retrieves a collection of all entities within the repository
     *
     * @return the entities within the repository
     */
    @SuppressWarnings("unchecked")
    public Collection<T> findAll() {
        List<T> outbound = new ArrayList<>();
        List generic = currentSession.createCriteria(supportingClass).list();
        for (Object o : generic) {
            if (!supportingClass.isInstance(o))
                throw new RuntimeException("Underlying database did not return a proper result");
            outbound.add((T) o);
        }
        return outbound;
    }

    /**
     * Finds an entity by the key provided
     *
     * @param key the key to lookup the object by
     * @return the object, if found. Null if not found.
     */
    public T findByKey(Serializable key) {
        return currentSession.get(supportingClass, key);
    }

    /**
     * Adds an entity to the repository
     *
     * @param entity the entity to add, cannot be null
     */
    public void add(T entity) {
        currentSession.save(entity);
    }

    /**
     * Deletes an entity from the repository
     *
     * @param entity the entity to delete, cannot be null
     */
    public void delete(T entity) {
        currentSession.delete(entity);
    }

    /**
     * Saves an entity that has already been added to the repository
     *
     * @param entity the entity to be saved, cannot be null
     */
    public void save(T entity) {
        currentSession.update(entity);
    }

    private static String readInitScript() throws IOException {
        String output = "";
        BufferedReader reader = new BufferedReader(new InputStreamReader(Repository.class.getResourceAsStream("/initdb.sql")));
        String line;
        while ((line = reader.readLine()) != null)
            output += line + "\n";
        return output;
    }
}
