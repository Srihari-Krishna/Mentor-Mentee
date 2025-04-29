package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.Session;
import com.example.mentormenteemanagement.repository.SessionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DefaultMentorRankCalculator implements MentorRankCalculator {

    @Autowired
    private SessionRepository sessionRepository;
    
    @Override
    public Map<Long, Integer> calculateMentorRanks() {
        List<Session> allSessions = sessionRepository.findAll();
        Map<Long, Integer> ranks = new HashMap<>();
        for (Session s : allSessions) {
            Long mid = s.getMentor().getId();
            ranks.put(mid, ranks.getOrDefault(mid, 0) + 1);
        }
        return ranks;
    }
}