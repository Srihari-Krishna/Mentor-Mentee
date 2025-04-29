package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.repository.MentorRepository;
import com.example.mentormenteemanagement.service.SessionService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/mentor")
public class MentorScheduleController {

    @Autowired
    private MentorRepository mentorRepository;
    
    @Autowired
    private MenteeRepository menteeRepository;
    
    @Autowired
    private SessionService sessionService;
    
    // Display scheduling page for mentor's own mentees
    @GetMapping("/schedule")
    public String showSchedulePage(HttpSession session, Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        
        Optional<Mentor> mentorOpt = mentorRepository.findByName(user.getUsername());
        if (!mentorOpt.isPresent()) {
            model.addAttribute("error", "Mentor profile not found.");
            return "scheduleSession";
        }
        Mentor mentor = mentorOpt.get();
        List<Mentee> mentees = menteeRepository.findByMentor_Id(mentor.getId());
        
        // Prepare session info for each mentee
        List<MentorScheduleController.MenteeSessionInfo> menteeInfos = new ArrayList<>();
        for (Mentee mentee : mentees) {
            int allowed = mentee.getAttendance() < 75 ? 3 : 2;
            int scheduled = sessionService.countSessionsForMentee(mentee.getId());
            int remaining = allowed - scheduled;
            MenteeSessionInfo info = new MenteeSessionInfo(mentee, allowed, scheduled, remaining);
            menteeInfos.add(info);
        }
        model.addAttribute("menteeInfos", menteeInfos);
        return "scheduleSession";
    }
    
    // Process scheduling form submission with duration input
    @PostMapping("/schedule")
    public String scheduleSession(@RequestParam Long menteeId,
                                  @RequestParam @DateTimeFormat(pattern="yyyy-MM-dd'T'HH:mm") LocalDateTime scheduledTime,
                                  @RequestParam int duration,
                                  HttpSession session,
                                  Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        
        Optional<Mentor> mentorOpt = mentorRepository.findByName(user.getUsername());
        if (!mentorOpt.isPresent()) {
            model.addAttribute("error", "Mentor profile not found.");
            return "scheduleSession";
        }
        Long mentorId = mentorOpt.get().getId();
        var scheduledSession = sessionService.scheduleSession(mentorId, menteeId, scheduledTime, duration);
        if (scheduledSession == null) {
            model.addAttribute("error", "Failed to schedule session. Either maximum sessions reached or an error occurred.");
        } else {
            model.addAttribute("success", "Session scheduled successfully for " + scheduledTime + " with duration " + duration + " min.");
        }
        return "redirect:/mentor/schedule";
    }
    
    // DTO for mentee session info
    public static class MenteeSessionInfo {
        private Mentee mentee;
        private int allowedSessions;
        private int scheduledSessions;
        private int remainingSessions;
        
        public MenteeSessionInfo(Mentee mentee, int allowedSessions, int scheduledSessions, int remainingSessions) {
            this.mentee = mentee;
            this.allowedSessions = allowedSessions;
            this.scheduledSessions = scheduledSessions;
            this.remainingSessions = remainingSessions;
        }
        // Getters and setters
        public Mentee getMentee() { return mentee; }
        public void setMentee(Mentee mentee) { this.mentee = mentee; }
        public int getAllowedSessions() { return allowedSessions; }
        public void setAllowedSessions(int allowedSessions) { this.allowedSessions = allowedSessions; }
        public int getScheduledSessions() { return scheduledSessions; }
        public void setScheduledSessions(int scheduledSessions) { this.scheduledSessions = scheduledSessions; }
        public int getRemainingSessions() { return remainingSessions; }
        public void setRemainingSessions(int remainingSessions) { this.remainingSessions = remainingSessions; }
    }
}
