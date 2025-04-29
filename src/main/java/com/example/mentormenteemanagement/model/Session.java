package com.example.mentormenteemanagement.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@Table(name = "sessions")
public class Session {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // The mentor scheduling the session
    @ManyToOne
    @JoinColumn(name = "mentor_id", nullable = false)
    private Mentor mentor;

    // The mentee for whom the session is scheduled
    @ManyToOne
    @JoinColumn(name = "mentee_id", nullable = false)
    private Mentee mentee;

    // Scheduled date and time
    @Column(nullable = false)
    private LocalDateTime scheduledTime;

    // Duration in minutes (capped at 20)
    @Column(nullable = false)
    private int duration = 20;

    // Flag to mark if the session has been completed
    @Column(nullable = false)
    private boolean completed = false;
    
    // Mentor feedback (null until provided)
    @Column(length = 1000)
    private String mentorFeedback;
    
    // Mentee feedback (null until provided)
    @Column(length = 1000)
    private String menteeFeedback;
}
