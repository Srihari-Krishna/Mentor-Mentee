package com.example.mentormenteemanagement.repository;

import com.example.mentormenteemanagement.model.Mentor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;
@Repository
public interface MentorRepository extends JpaRepository<Mentor, Long> {
    List<Mentor> findByNameContainingIgnoreCase(String name);
    Optional<Mentor> findByName(String name);
}
