package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.builder.SessionBuilder;
import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.model.Session;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.repository.MentorRepository;
import com.example.mentormenteemanagement.repository.SessionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class SessionServiceImpl implements SessionService {

    @Autowired
    private SessionRepository sessionRepository;

    @Autowired
    private MenteeRepository menteeRepository;

    @Autowired
    private MentorRepository mentorRepository;

    @Override
    @Transactional
    public Session scheduleSession(Long mentorId, Long menteeId, LocalDateTime scheduledTime, int duration) {
        // Cap duration to 20 minutes
        if (duration > 20) {
            duration = 20;
        }

        Optional<Mentee> menteeOpt = menteeRepository.findById(menteeId);
        if (!menteeOpt.isPresent()) {
            return null;
        }
        Mentee mentee = menteeOpt.get();
        int maxSessions = mentee.getAttendance() < 75 ? 3 : 2;
        int scheduledCount = countSessionsForMentee(menteeId);
        if (scheduledCount >= maxSessions) {
            return null;
        }

        Optional<Mentor> mentorOpt = mentorRepository.findById(mentorId);
        if (!mentorOpt.isPresent()) {
            return null;
        }
        Mentor mentor = mentorOpt.get();

        // Create Session using the SessionBuilder
        Session session = new SessionBuilder()
                .withMentor(mentor)
                .withMentee(mentee)
                .withScheduledTime(scheduledTime)
                .withDuration(duration)
                .build();

        Session savedSession = sessionRepository.save(session);

        // Update mentor's earnings and points at scheduling time (if desired)
        double earning = (duration / 20.0) * 30.0;
        mentor.setEarnings(mentor.getEarnings() + earning);
        mentor.setPoints(mentor.getPoints() + 1);
        mentorRepository.save(mentor);

        return savedSession;
    }

    @Override
    public int countSessionsForMentee(Long menteeId) {
        return sessionRepository.countByMentee_Id(menteeId);
    }

    // Scheduled task to mark sessions as completed once their end time has passed
    @Scheduled(fixedDelay = 60000) // every minute
    @Transactional
    public void completeSessions() {
        LocalDateTime now = LocalDateTime.now();
        List<Session> sessions = sessionRepository.findAll(); // Alternatively, filter by completed = false
        for (Session session : sessions) {
            if (!session.isCompleted()) {
                LocalDateTime sessionEnd = session.getScheduledTime().plusMinutes(session.getDuration());
                if (sessionEnd.isBefore(now)) {
                    // Mark session as completed
                    session.setCompleted(true);
                    sessionRepository.save(session);

                    // Update mentor's sessions conducted
                    Mentor mentor = session.getMentor();
                    mentor.setSessionsConducted(mentor.getSessionsConducted() + 1);
                    mentorRepository.save(mentor);
                }
            }
        }
    }
}
