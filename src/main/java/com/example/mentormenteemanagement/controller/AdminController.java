package com.example.mentormenteemanagement.controller;

import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.Mentor;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.service.AssignmentService;
import com.example.mentormenteemanagement.service.UserSearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin")
public class AdminController {

    @Autowired
    private AssignmentService assignmentService;

    @Autowired
    private MenteeRepository menteeRepository;

    @Autowired
    @Qualifier("mentorSearchServiceImpl")
    private UserSearchService<Mentor> mentorSearchService;

    @Autowired
    @Qualifier("menteeSearchServiceImpl")
    private UserSearchService<Mentee> menteeSearchService;

    // Existing assignment endpoint: shows assignment page with all mentors and
    // unassigned mentees
    @GetMapping("/assign")
    public String showAssignmentPage(Model model) {
        model.addAttribute("mentors", assignmentService.getAllMentors());
        model.addAttribute("unassignedMentees", assignmentService.getUnassignedMentees());
        return "assignment";
    }

    @PostMapping("/assign")
    public String assignMentee(@RequestParam Long menteeId,
            @RequestParam Long mentorId,
            Model model) {
        boolean assigned = assignmentService.assignMenteeToMentor(menteeId, mentorId);
        if (assigned) {
            model.addAttribute("message", "Mentee assigned successfully!");
        } else {
            model.addAttribute("error",
                    "Assignment failed! Mentor may have reached maximum capacity or an error occurred.");
        }
        model.addAttribute("mentors", assignmentService.getAllMentors());
        model.addAttribute("unassignedMentees", assignmentService.getUnassignedMentees());
        return "assignment";
    }

    // New endpoint to filter unassigned mentees by year.
    @GetMapping("/menteesByYear")
    @ResponseBody
    public List<Mentee> getMenteesByYear(@RequestParam int year) {
        return menteeRepository.findByYearAndMentorIsNull(year);
    }

    // Updated search endpoint using UserSearchService implementations
    @GetMapping("/search")
    public String search(@RequestParam(required = false) String type,
            @RequestParam(required = false) String query,
            Model model) {
        if (query != null && type != null) {
            if (type.equalsIgnoreCase("mentor")) {
                List<Mentor> mentors = mentorSearchService.searchByName(query);
                model.addAttribute("mentors", mentors);
            } else if (type.equalsIgnoreCase("mentee")) {
                List<Mentee> mentees = menteeSearchService.searchByName(query);
                model.addAttribute("mentees", mentees);
            }
            model.addAttribute("query", query);
            model.addAttribute("type", type);
        }
        return "adminSearch";
    }
}
