package com.example.mentormenteemanagement.service;

// import com.example.mentormenteemanagement.model.Mentor;
import java.util.Map;

public interface MentorRankCalculator {
    // Calculate mentor ranking (e.g. total session count)
    Map<Long, Integer> calculateMentorRanks();
}