package com.example.mentormenteemanagement.service;

public interface MenteeFeedbackService {
    boolean submitFeedback(Long sessionId, String feedback);
}