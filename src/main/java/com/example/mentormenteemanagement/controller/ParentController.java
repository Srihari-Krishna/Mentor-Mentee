package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Session;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.repository.SessionRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.ArrayList;
import java.util.List;

@Controller
public class ParentController {

    @Autowired
    private MenteeRepository menteeRepository;

    @Autowired
    private SessionRepository sessionRepository;

    @GetMapping("/parent/childProgress")
    public String viewChildProgress(HttpSession httpSession, Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("PARENT")) {
            return "redirect:/login";
        }

        List<Mentee> children = menteeRepository.findByParent_Id(user.getId());
        if (children.isEmpty()) {
            model.addAttribute("error", "No child linked to your account.");
        } else {
            model.addAttribute("children", children);
        }
        return "parentChildProgress";
    }

    @GetMapping("/parent/mentorReviews")
    public String viewMentorReviews(HttpSession httpSession, Model model) {
        User user = (User) httpSession.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("PARENT")) {
            return "redirect:/login";
        }

        // Fetch all children for this parent
        List<Mentee> children = menteeRepository.findByParent_Id(user.getId());
        if (children.isEmpty()) {
            model.addAttribute("error", "No child linked to your account.");
            return "parentMentorReviews";
        }

        // Gather all completed sessions for each child
        List<Session> reviews = new ArrayList<>();
        for (Mentee child : children) {
            reviews.addAll(
                sessionRepository.findByMentee_IdAndCompletedTrue(child.getId())
            );
        }

        model.addAttribute("reviews", reviews);
        return "parentMentorReviews";
    }
}
