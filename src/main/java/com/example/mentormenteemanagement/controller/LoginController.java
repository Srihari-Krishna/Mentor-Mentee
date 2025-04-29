package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.flyweight.RoleIconFactory;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.service.UserService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class LoginController {

    @Autowired
    private UserService userService;

    @GetMapping({ "/", "/login" })
    public String showLoginPage() {
        return "login"; // Thymeleaf template: src/main/resources/templates/login.html
    }

    @PostMapping("/login")
    public String doLogin(@RequestParam("username") String username,
            @RequestParam("password") String password,
            @RequestParam("role") String role,
            HttpSession session,
            Model model) {

        User user = userService.login(username, password, role);

        if (user != null) {
            session.setAttribute("user", user); // Save user to session

            // Use Flyweight pattern to retrieve the role icon for the logged-in user.
            String roleIcon = RoleIconFactory.getRoleIcon(user.getRole()).getIcon();
            model.addAttribute("roleIcon", roleIcon);

            switch (user.getRole().toUpperCase()) {
                case "ADMIN":
                    return "adminHome"; // Thymeleaf template: src/main/resources/templates/adminHome.html
                case "MENTOR":
                    return "redirect:/mentor/home";
                case "MENTEE":
                    return "redirect:/mentee/home";
                case "PARENT":
                    return "redirect:/parent/home";
                default:
                    return "redirect:/dashboard"; // fallback for unknown roles
            }
        } else {
            model.addAttribute("error", "Invalid credentials! Please try again.");
            return "login";
        }
    }
}
