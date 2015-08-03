package ca.ents.simon.repository.concrete;


import ca.ents.simon.entities.Entity;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;
import org.reflections.Reflections;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public abstract class Repository<T extends Entity> implements ca.ents.simon.repository.Repository<T> {

    private final static SessionFactory SESSION_FACTORY;
    private Session currentSession;
    private Class<T> supportingClass;

    static {
        Configuration hibernateConf = new Configuration();

        // General properties
        hibernateConf.setProperty("hibernate.connection.provider_class", "com.zaxxer.hikari.hibernate.HikariConnectionProvider");
        hibernateConf.setProperty("hibernate.hikari.dataSourceClassName", "com.mysql.jdbc.jdbc2.optional.MysqlDataSource");
        hibernateConf.setProperty("hibernate.hikari.dataSource.url", "jdbc:mysql://172.16.0.26/simon");
        hibernateConf.setProperty("hibernate.hikari.dataSource.user", "simon");
        hibernateConf.setProperty("hibernate.hikari.dataSource.password", "test1234");
        hibernateConf.setProperty("hibernate.hikari.dataSource.cachePrepStmts", "true");
        hibernateConf.setProperty("hibernate.hikari.dataSource.prepStmtCacheSize", "250");
        hibernateConf.setProperty("hibernate.hikari.dataSource.prepStmtCacheSqlLimit", "2048");

        // Setup mappings
        Reflections reflections = new Reflections(Entity.class.getPackage().getName());
        reflections.getSubTypesOf(Entity.class).forEach(hibernateConf::addClass);

        // Configure and set session factory
        ServiceRegistry serviceRegistry = new StandardServiceRegistryBuilder().applySettings(hibernateConf.getProperties()).build();
        SESSION_FACTORY = hibernateConf.buildSessionFactory(serviceRegistry);
    }

    protected Repository(Class<T> supportingClass) {
        currentSession = SESSION_FACTORY.openSession();
        this.supportingClass = supportingClass;
    }

    @Override
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

    @Override
    public T findByKey(Serializable key) {
        return currentSession.get(supportingClass, key);
    }

    @Override
    public void add(T entity) {
        currentSession.save(entity);
    }

    @Override
    public void delete(T entity) {
        currentSession.delete(entity);
    }

    @Override
    public void save(T entity) {
        currentSession.update(entity);
    }
}
