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
public class MentorSessionController {

    @Autowired
    private SessionRepository sessionRepository;

    @Autowired
    private MentorRepository mentorRepository;

    // Display session info with optional filtering by mentee id
    @GetMapping("/sessions")
    public String viewSessions(@RequestParam(required = false) Long menteeId, HttpSession httpSession, Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        // Retrieve mentor record based on logged-in username
        Optional<Mentor> mentorOpt = mentorRepository.findByName(user.getUsername());
        if (!mentorOpt.isPresent()) {
            model.addAttribute("error", "Mentor profile not found.");
            return "mentorSessions";
        }
        Mentor mentor = mentorOpt.get();
        List<Session> sessions = sessionRepository.findByMentor_Id(mentor.getId());
        // Filter sessions by menteeId if provided
        if (menteeId != null) {
            sessions = sessions.stream()
                    .filter(s -> s.getMentee() != null && s.getMentee().getId().equals(menteeId))
                    .collect(Collectors.toList());
        }
        model.addAttribute("sessions", sessions);
        return "mentorSessions";
    }

    // Display a form to edit/add mentor feedback for a session
    @GetMapping("/sessions/edit/{sessionId}")
    public String editFeedback(@PathVariable Long sessionId, HttpSession httpSession, Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        Optional<Session> sessionOpt = sessionRepository.findById(sessionId);
        if (!sessionOpt.isPresent()) {
            model.addAttribute("error", "Session not found.");
            return "mentorEditFeedback";
        }
        model.addAttribute("sessionObj", sessionOpt.get());
        return "mentorEditFeedback";
    }

    // Process mentor feedback update
    @PostMapping("/sessions/edit/{sessionId}")
    public String updateFeedback(@PathVariable Long sessionId, @RequestParam String mentorFeedback, HttpSession httpSession, Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        Optional<Session> sessionOpt = sessionRepository.findById(sessionId);
        if (!sessionOpt.isPresent()) {
            model.addAttribute("error", "Session not found.");
            return "mentorEditFeedback";
        }
        Session sess = sessionOpt.get();
        sess.setMentorFeedback(mentorFeedback);
        sessionRepository.save(sess);
        return "redirect:/mentor/sessions";
    }
}
