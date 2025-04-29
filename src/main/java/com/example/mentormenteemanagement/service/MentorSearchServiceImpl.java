package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.repository.MentorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class MentorSearchServiceImpl implements UserSearchService<Mentor> {

    @Autowired
    private MentorRepository mentorRepository;
    
    @Override
    public List<Mentor> searchByName(String name) {
        return mentorRepository.findByNameContainingIgnoreCase(name);
    }
}