package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.Session;
import com.example.mentormenteemanagement.repository.SessionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class MenteeFeedbackServiceImpl implements MenteeFeedbackService {

    @Autowired
    private SessionRepository sessionRepository;
    
    @Override
    public boolean submitFeedback(Long sessionId, String feedback) {
        Optional<Session> sessionOpt = sessionRepository.findById(sessionId);
        if(sessionOpt.isPresent()){
            Session session = sessionOpt.get();
            session.setMenteeFeedback(feedback);
            sessionRepository.save(session);
            return true;
        }
        return false;
    }
}