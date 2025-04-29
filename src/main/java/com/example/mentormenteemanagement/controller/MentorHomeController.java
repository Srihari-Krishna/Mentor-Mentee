package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.flyweight.RoleIconFactory;
import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.repository.MentorRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import java.util.List;
import java.util.Optional;

@Controller
public class MentorHomeController {

    @Autowired
    private MentorRepository mentorRepository;

    @Autowired
    private MenteeRepository menteeRepository;

    @GetMapping("/mentor/home")
    public String showMentorHome(HttpSession session, Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        model.addAttribute("username", user.getUsername());
        // Add role icon using Flyweight pattern
        String roleIcon = RoleIconFactory.getRoleIcon(user.getRole()).getIcon();
        model.addAttribute("roleIcon", roleIcon);
        return "mentorHome";
    }

    @GetMapping("/mentor/mentees")
    public String viewMentees(HttpSession session, Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTOR")) {
            return "redirect:/login";
        }
        // Add role icon using Flyweight pattern
        String roleIcon = RoleIconFactory.getRoleIcon(user.getRole()).getIcon();
        model.addAttribute("roleIcon", roleIcon);

        Optional<Mentor> mentorOpt = mentorRepository.findByName(user.getUsername());
        if (!mentorOpt.isPresent()) {
            model.addAttribute("error", "No mentor profile found for your account.");
            model.addAttribute("mentees", null);
            return "mentorMentees";
        }
        Mentor mentor = mentorOpt.get();
        List<Mentee> mentees = menteeRepository.findByMentor_Id(mentor.getId());
        model.addAttribute("mentees", mentees);
        return "mentorMentees";
    }
}
