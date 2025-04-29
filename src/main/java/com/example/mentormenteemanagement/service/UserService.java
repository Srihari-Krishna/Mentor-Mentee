package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.User;

public interface UserService {
    User login(String username, String password, String role);
    boolean registerMentee(String username, String password, double cgpa, int year);
    boolean registerParent(String username, String password, Long menteeId);
}
