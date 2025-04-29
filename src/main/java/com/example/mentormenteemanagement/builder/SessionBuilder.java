package com.example.mentormenteemanagement.builder;

import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Session;

import java.time.LocalDateTime;

public class SessionBuilder {
    private Mentor mentor;
    private Mentee mentee;
    private LocalDateTime scheduledTime;
    private int duration = 20; // default capped duration
    private boolean completed = false;

    public SessionBuilder withMentor(Mentor mentor) {
        this.mentor = mentor;
        return this;
    }

    public SessionBuilder withMentee(Mentee mentee) {
        this.mentee = mentee;
        return this;
    }

    public SessionBuilder withScheduledTime(LocalDateTime scheduledTime) {
        this.scheduledTime = scheduledTime;
        return this;
    }

    public SessionBuilder withDuration(int duration) {
        this.duration = Math.min(duration, 20);
        return this;
    }

    public Session build() {
        Session session = new Session();
        session.setMentor(mentor);
        session.setMentee(mentee);
        session.setScheduledTime(scheduledTime);
        session.setDuration(duration);
        session.setCompleted(completed);
        return session;
    }
}