package ca.ents.simon.util;

import javafx.scene.Group;
import javafx.scene.Node;

/**
 * Represents a group of UI components to provide an easy to use interface for UI building
 */
public class UIGroup {

    private Group group;

    public UIGroup(Group group) {
        if (group == null) throw new IllegalArgumentException("Group cannot be null");
        this.group = group;
    }

    /**
     * Adds a child node to this UI group
     *
     * @param child the child to add, cannot be null
     * @return the current UI group
     */
    public UIGroup addChild(Node child) {
        if (child == null) throw new IllegalArgumentException("Child cannot be null");
        group.getChildren().add(child);
        return this;
    }

    /**
     * Attempts to find a child node for the given ID. If the ID is not found, or null, this returns null.
     *
     * @param id the ID to lookup, should not be null
     * @return the node found, or null if the ID is null or not found
     */
    public Node findById(String id) {
        if (id == null) return null;
        for (Node child : group.getChildren()) {
            if (child.getId() != null && child.getId().equals(id))
                return child;
        }
        return null;
    }
}
