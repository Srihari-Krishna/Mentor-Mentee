package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.Mentee;
//import com.example.mentormenteemanagement.repository.MenteeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class MenteeSearchServiceImpl implements UserSearchService<Mentee> {

    @Autowired
    private com.example.mentormenteemanagement.repository.MenteeRepository menteeRepository;
    
    @Override
    public List<Mentee> searchByName(String name) {
        return menteeRepository.findByNameContainingIgnoreCase(name);
    }
}