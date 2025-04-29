package com.example.mentormenteemanagement.factory;

import com.example.mentormenteemanagement.model.User;

public class UserFactory {
    public static User createUser(String username, String password, String role) {
        User user = new User();
        user.setUsername(username);
        user.setPassword(password);
        user.setRole(role.toUpperCase()); // Ensure role consistency
        return user;
    }
}