package com.example.mentormenteemanagement.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
@Table(name = "mentors")
public class Mentor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Mentor's full name
    @Column(nullable = false)
    private String name;

    // e.g., Assistant Prof, Professor, etc.
    @Column(nullable = false)
    private String role;

    // Maximum number of mentees allowed
    @Column(nullable = false)
    private int maxMentees;

    // Total sessions conducted (initially 0)
    @Column(nullable = false)
    private int sessionsConducted;

    // Earnings from sessions (initially 0)
    @Column(nullable = false)
    private double earnings;

    // Gamification score/points (initially 0)
    @Column(nullable = false)
    private int points;

    // Mentor can only mentor students of a specific academic year
    @Column(nullable = false)
    private int yearCanMentor;
}
