package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class RegisterController {

    @Autowired
    private UserService userService;

    @GetMapping("/register")
    public String showRegisterPage() {
        return "register";
    }

    @PostMapping("/register")
    public String doRegister(@RequestParam String username,
                             @RequestParam String password,
                             @RequestParam String role,
                             // Mentee-specific parameters
                             @RequestParam(required = false) Double cgpa,
                             @RequestParam(required = false) Integer year,
                             // Parent-specific parameter
                             @RequestParam(required = false) Long menteeId,
                             Model model) {
        boolean success = false;
        if (role.equalsIgnoreCase("MENTEE")) {
            if (cgpa == null || year == null) {
                model.addAttribute("error", "Please provide CGPA and Year for Mentee registration.");
                return "register";
            }
            success = userService.registerMentee(username, password, cgpa, year);
        } else if (role.equalsIgnoreCase("PARENT")) {
            if (menteeId == null) {
                model.addAttribute("error", "Please provide the associated Mentee ID for Parent registration.");
                return "register";
            }
            success = userService.registerParent(username, password, menteeId);
        } else {
            model.addAttribute("error", "Registration is only allowed for Mentees or Parents.");
            return "register";
        }
        if (success) {
            model.addAttribute("success", "Registration successful! You can now log in.");
        } else {
            model.addAttribute("error", "Registration failed! Either the username exists or the associated Mentee was not found.");
        }
        return "register";
    }
}
