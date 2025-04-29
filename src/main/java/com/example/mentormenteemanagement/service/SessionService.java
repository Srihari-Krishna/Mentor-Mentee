package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.model.Session;
import java.time.LocalDateTime;

public interface SessionService {
    // Now accepts a duration (in minutes) parameter
    Session scheduleSession(Long mentorId, Long menteeId, LocalDateTime scheduledTime, int duration);
    
    int countSessionsForMentee(Long menteeId);
}
