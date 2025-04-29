package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Session;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.repository.SessionRepository;
import com.example.mentormenteemanagement.service.MenteeFeedbackService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/mentee")
public class MenteeSessionController {

    @Autowired
    private SessionRepository sessionRepository;

    @Autowired
    private MenteeRepository menteeRepository;

    @Autowired
    private MenteeFeedbackService menteeFeedbackService;

    // Show all completed sessions for the logged-in mentee, filter by optional
    // menteeId (should be their own)
    @GetMapping("/sessions")
    public String viewSessions(@RequestParam(required = false) Long menteeId,
            HttpSession httpSession,
            Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTEE")) {
            return "redirect:/login";
        }
        // Find the Mentee entity by username
        Optional<Mentee> menteeOpt = menteeRepository.findByName(user.getUsername());
        if (!menteeOpt.isPresent()) {
            model.addAttribute("error", "Mentee profile not found.");
            return "menteeSessions";
        }
        Long myId = menteeOpt.get().getId();
        // If menteeId param is provided but doesn’t match the logged-in mentee, ignore
        // it
        if (menteeId == null || !menteeId.equals(myId)) {
            menteeId = myId;
        }

        List<Session> sessions = sessionRepository.findByMentee_IdAndCompletedTrue(menteeId);
        model.addAttribute("sessions", sessions);
        return "menteeSessions";
    }

    // Show form to give or edit mentee feedback
    @GetMapping("/sessions/edit/{sessionId}")
    public String showFeedbackForm(@PathVariable Long sessionId,
            HttpSession httpSession,
            Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTEE")) {
            return "redirect:/login";
        }
        Optional<Session> sessionOpt = sessionRepository.findById(sessionId);
        if (!sessionOpt.isPresent()) {
            model.addAttribute("error", "Session not found.");
            return "menteeFeedbackForm";
        }
        Session sess = sessionOpt.get();
        // ensure this session belongs to the logged-in mentee
        if (!sess.getMentee().getName().equals(user.getUsername())) {
            return "redirect:/mentee/sessions";
        }
        model.addAttribute("sessionObj", sess);
        return "menteeFeedbackForm";
    }

    // Process mentee feedback submission using the MenteeFeedbackService
    // abstraction
    @PostMapping("/sessions/edit/{sessionId}")
    public String submitFeedback(@PathVariable Long sessionId,
            @RequestParam String menteeFeedback,
            HttpSession httpSession,
            Model model) {
        boolean success = menteeFeedbackService.submitFeedback(sessionId, menteeFeedback);
        if (!success) {
            model.addAttribute("error", "Session not found.");
        }
        return "redirect:/mentee/sessions";
    }

    @GetMapping("/upcoming")
    public String viewUpcomingSessions(HttpSession httpSession, Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTEE")) {
            return "redirect:/login";
        }

        // look up the Mentee record for this user
        Optional<Mentee> meOpt = menteeRepository.findByName(user.getUsername());
        if (!meOpt.isPresent()) {
            model.addAttribute("error", "Mentee profile not found.");
            return "menteeUpcoming";
        }
        Long myId = meOpt.get().getId();

        // fetch all not-yet-completed sessions scheduled after now
        List<Session> upcoming = sessionRepository
                .findByMentee_IdAndCompletedFalseAndScheduledTimeAfter(myId, LocalDateTime.now());

        model.addAttribute("upcomingSessions", upcoming);
        return "menteeUpcoming";
    }
}
