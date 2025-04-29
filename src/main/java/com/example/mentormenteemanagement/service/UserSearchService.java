package com.example.mentormenteemanagement.service;

import java.util.List;

public interface UserSearchService<T> {
    List<T> searchByName(String name);
}