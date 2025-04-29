package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.model.User;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class AdminHomeController {

    @GetMapping("/admin/home")
    public String showAdminHome(HttpSession session, Model model) {
        User user = (User) session.getAttribute("user");
        if (user == null || !user.getRole().equalsIgnoreCase("ADMIN")) {
            System.out.println(user);
            return "redirect:/login";
        }
        model.addAttribute("username", user.getUsername());
        return "adminHome";
    }
}
