package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.flyweight.RoleIconFactory;
import com.example.mentormenteemanagement.model.User;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MenteeHomeController {

    @GetMapping("/mentee/home")
    public String showMenteeHome(HttpSession session, Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("MENTEE")) {
            return "redirect:/login";
        }
        model.addAttribute("username", user.getUsername());
        // Add role icon using Flyweight pattern
        String roleIcon = RoleIconFactory.getRoleIcon(user.getRole()).getIcon();
        model.addAttribute("roleIcon", roleIcon);
        return "menteeHome";
    }
}
