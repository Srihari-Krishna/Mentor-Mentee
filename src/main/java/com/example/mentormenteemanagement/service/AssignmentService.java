package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Mentor;
import java.util.List;

public interface AssignmentService {
    List<Mentor> getAllMentors();
    List<Mentee> getUnassignedMentees();
    boolean assignMenteeToMentor(Long menteeId, Long mentorId);
    
    // New search methods:
    List<Mentor> searchMentorsByName(String name);
    List<Mentee> searchMenteesByName(String name);
}
