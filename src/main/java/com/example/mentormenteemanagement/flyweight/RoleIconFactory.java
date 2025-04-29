// filepath: src/main/java/com/example/mentormenteemanagement/flyweight/RoleIconFactory.java
package com.example.mentormenteemanagement.flyweight;

import java.util.HashMap;
import java.util.Map;

public class RoleIconFactory {
    private static final Map<String, RoleIcon> roleIconMap = new HashMap<>();
    
    // Returns a flyweight RoleIcon for a given role
    public static RoleIcon getRoleIcon(String role) {
        String normalized = role.toUpperCase();
        if (!roleIconMap.containsKey(normalized)) {
            // For example, assign icons (could be CSS classes or image paths)
            String icon;
            switch(normalized) {
                case "ADMIN":
                    icon = "fa-shield-alt";
                    break;
                case "MENTOR":
                    icon = "fa-chalkboard-teacher";
                    break;
                case "MENTEE":
                    icon = "fa-user-graduate";
                    break;
                case "PARENT":
                    icon = "fa-user-friends";
                    break;
                default:
                    icon = "fa-user";
            }
            roleIconMap.put(normalized, new RoleIcon(icon));
        }
        return roleIconMap.get(normalized);
    }
}