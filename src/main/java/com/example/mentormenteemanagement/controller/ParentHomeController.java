package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.flyweight.RoleIconFactory;
import com.example.mentormenteemanagement.model.User;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class ParentHomeController {

    @GetMapping("/parent/home")
    public String showParentHome(HttpSession session, Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("PARENT")) {
            return "redirect:/login";
        }
        model.addAttribute("username", user.getUsername());
        // Add role icon using Flyweight pattern
        String roleIcon = RoleIconFactory.getRoleIcon(user.getRole()).getIcon();
        model.addAttribute("roleIcon", roleIcon);
        return "parentHome";
    }
}
