package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.repository.MentorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class AssignmentServiceImpl implements AssignmentService {

    @Autowired
    private MentorRepository mentorRepository;

    @Autowired
    private MenteeRepository menteeRepository;

    @Override
    public List<Mentor> getAllMentors() {
        return mentorRepository.findAll();
    }

    @Override
    public List<Mentee> getUnassignedMentees() {
        return menteeRepository.findByMentorIsNull();
    }

    @Override
    public boolean assignMenteeToMentor(Long menteeId, Long mentorId) {
        Optional<Mentee> menteeOpt = menteeRepository.findById(menteeId);
        Optional<Mentor> mentorOpt = mentorRepository.findById(mentorId);
        if (menteeOpt.isPresent() && mentorOpt.isPresent()) {
            Mentor mentor = mentorOpt.get();
            int assignedCount = menteeRepository.countByMentorId(mentorId);
            if (assignedCount >= mentor.getMaxMentees()) {
                return false;
            }
            Mentee mentee = menteeOpt.get();
            mentee.setMentor(mentor);
            menteeRepository.save(mentee);
            return true;
        }
        return false;
    }

    @Override
    public List<Mentor> searchMentorsByName(String name) {
        return mentorRepository.findByNameContainingIgnoreCase(name);
    }

    @Override
    public List<Mentee> searchMenteesByName(String name) {
        return menteeRepository.findByNameContainingIgnoreCase(name);
    }
}
