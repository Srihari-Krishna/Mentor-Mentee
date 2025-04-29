package com.example.mentormenteemanagement.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
@Table(name = "mentees")
public class Mentee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Mentee's name (using username upon registration)
    @Column(nullable = false)
    private String name;

    // Link to assigned mentor (nullable if not assigned)
    @ManyToOne
    @JoinColumn(name = "mentor_id")
    private Mentor mentor;

    // Academic details
    @Column(nullable = false)
    private double cgpa;

    @Column(nullable = false)
    private int isaMarks;

    // Year of study
    @Column(nullable = false)
    private int year;

    // Attendance percentage (default 100)
    @Column(nullable = false)
    private float attendance = 100.0f;
    
    // Optional link to parent's details (a User with role "PARENT")
    @ManyToOne
    @JoinColumn(name = "parent_id")
    private User parent;
}
