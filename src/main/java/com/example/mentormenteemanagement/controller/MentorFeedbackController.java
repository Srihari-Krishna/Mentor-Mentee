package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.model.Session;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.repository.MentorRepository;
import com.example.mentormenteemanagement.repository.SessionRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/mentor")
public class MentorFeedbackController {

    @Autowired
    private MentorRepository mentorRepository;
    
    @Autowired
    private SessionRepository sessionRepository;
    
    // Display list of completed sessions that still lack mentor feedback
    @GetMapping("/feedback/pending")
    public String viewPendingFeedback(HttpSession session, Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        // Retrieve mentor record by matching username
        Optional<Mentor> mentorOpt = mentorRepository.findByName(user.getUsername());
        if (!mentorOpt.isPresent()) {
            model.addAttribute("error", "Mentor profile not found.");
            return "mentorPendingFeedback";
        }
        Mentor mentor = mentorOpt.get();
        // Get all sessions for this mentor that are completed
        List<Session> completedSessions = sessionRepository.findByMentor_IdAndCompletedTrue(mentor.getId());
        // Filter sessions where mentor feedback is missing
        List<Session> pendingSessions = completedSessions.stream()
                .filter(s -> s.getMentorFeedback() == null || s.getMentorFeedback().isEmpty())
                .collect(Collectors.toList());
        model.addAttribute("pendingSessions", pendingSessions);
        return "mentorPendingFeedback";
    }
    
    // Display a page to submit feedback for a specific session
    @GetMapping("/feedback/submit/{sessionId}")
    public String showFeedbackForm(@PathVariable Long sessionId, HttpSession session, Model model) {
        // Check if session exists
        Optional<Session> sessionOpt = sessionRepository.findById(sessionId);
        if (!sessionOpt.isPresent()) {
            model.addAttribute("error", "Session not found.");
            return "mentorFeedbackForm";
        }
        model.addAttribute("sessionObj", sessionOpt.get());
        return "mentorFeedbackForm";
    }
    
    // Process mentor feedback submission
    @PostMapping("/feedback/submit/{sessionId}")
    public String submitFeedback(@PathVariable Long sessionId,
                                 @RequestParam String feedbackText,
                                 HttpSession httpSession,
                                 Model model) {
        Optional<Session> sessionOpt = sessionRepository.findById(sessionId);
        if (!sessionOpt.isPresent()) {
            model.addAttribute("error", "Session not found.");
            return "redirect:/mentor/feedback/pending";
        }
        Session sess = sessionOpt.get();
        sess.setMentorFeedback(feedbackText);
        sessionRepository.save(sess);
        model.addAttribute("success", "Feedback submitted successfully.");
        return "redirect:/mentor/feedback/pending";
    }
}
