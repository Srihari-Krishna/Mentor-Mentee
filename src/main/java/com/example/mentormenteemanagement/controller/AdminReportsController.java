package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.model.Session;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.repository.MentorRepository;
import com.example.mentormenteemanagement.repository.SessionRepository;
import com.example.mentormenteemanagement.service.MentorRankCalculator;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/admin")
public class AdminReportsController {

    @Autowired
    private MentorRepository mentorRepo;

    @Autowired
    private SessionRepository sessionRepo;

    @Autowired
    private MentorRankCalculator mentorRankCalculator;

    @GetMapping("/reports")
    public String showReports(HttpSession session, Model model) {
        User u = (User) session.getAttribute("user");
        if (u == null || !"ADMIN".equalsIgnoreCase(u.getRole())) {
            return "redirect:/login";
        }

        // 1) Load all mentors
        List<Mentor> mentors = mentorRepo.findAll();

        // 2) Load all sessions for additional computations
        List<Session> allSessions = sessionRepo.findAll();

        // 3) Compute per-mentor session counts with MentorRankCalculator (OCP
        // improvement)
        Map<Long, Integer> totalSessions = mentorRankCalculator.calculateMentorRanks();

        // 4) Compute total duration per mentor
        Map<Long, Integer> totalDuration = new HashMap<>();
        for (Session s : allSessions) {
            Long mid = s.getMentor().getId();
            totalDuration.put(mid, totalDuration.getOrDefault(mid, 0) + s.getDuration());
        }

        // 5) Sort mentors by session count descending
        mentors.sort(Comparator.comparing(
                (Mentor m) -> totalSessions.getOrDefault(m.getId(), 0))
                .reversed());

        // 6) Prepare chart data
        List<String> labels = mentors.stream()
                .map(Mentor::getName)
                .collect(Collectors.toList());
        List<Integer> durations = mentors.stream()
                .map(m -> totalDuration.getOrDefault(m.getId(), 0))
                .collect(Collectors.toList());

        // Pass data to the view
        model.addAttribute("mentors", mentors);
        model.addAttribute("totalSessions", totalSessions);
        model.addAttribute("totalDuration", totalDuration);
        model.addAttribute("labels", labels);
        model.addAttribute("durations", durations);

        return "adminReports";
    }

    @GetMapping("/reports/mentor/{mentorId}")
    public String showMentorDetail(@PathVariable Long mentorId,
            HttpSession session,
            Model model) {
        User u = (User) session.getAttribute("user");
        if (u == null || !"ADMIN".equalsIgnoreCase(u.getRole())) {
            return "redirect:/login";
        }
        List<Session> sessions = sessionRepo.findByMentor_Id(mentorId);
        model.addAttribute("sessions", sessions);
        return "adminReportDetail";
    }
}
