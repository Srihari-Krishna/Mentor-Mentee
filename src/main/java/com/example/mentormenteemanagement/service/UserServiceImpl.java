package com.example.mentormenteemanagement.service;

import com.example.mentormenteemanagement.factory.UserFactory; // added import for factory
import com.example.mentormenteemanagement.model.Mentee;
import com.example.mentormenteemanagement.model.User;
import com.example.mentormenteemanagement.repository.MenteeRepository;
import com.example.mentormenteemanagement.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserRepository userRepository;

    // Used for creating Mentee records
    @Autowired
    private MenteeRepository menteeRepository;

    @Override
    public User login(String username, String password, String role) {
        return userRepository.findByUsername(username)
                .filter(user -> user.getPassword().equals(password) &&
                        user.getRole().equalsIgnoreCase(role))
                .orElse(null);
    }

    @Override
    public boolean registerMentee(String username, String password, double cgpa, int year) {
        Optional<User> existingUser = userRepository.findByUsername(username);
        if (existingUser.isPresent()) {
            return false;
        }
        // Create User record with role MENTEE using UserFactory
        User newUser = UserFactory.createUser(username, password, "MENTEE");
        userRepository.save(newUser);

        // Create a corresponding Mentee record with provided details
        Mentee newMentee = new Mentee();
        newMentee.setName(username);
        newMentee.setCgpa(cgpa);
        newMentee.setYear(year);
        menteeRepository.save(newMentee);
        return true;
    }

    @Override
    public boolean registerParent(String username, String password, Long menteeId) {
        Optional<User> existingUser = userRepository.findByUsername(username);
        if (existingUser.isPresent()) {
            return false;
        }
        // Create User record with role PARENT using UserFactory
        User newUser = UserFactory.createUser(username, password, "PARENT");
        userRepository.save(newUser);

        // Link the Parent with an existing Mentee record
        Optional<Mentee> menteeOpt = menteeRepository.findById(menteeId);
        if (!menteeOpt.isPresent()) {
            return false;
        }
        Mentee mentee = menteeOpt.get();
        mentee.setParent(newUser);
        menteeRepository.save(mentee);
        return true;
    }
}
