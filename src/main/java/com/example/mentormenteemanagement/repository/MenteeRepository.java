package com.example.mentormenteemanagement.repository;

import com.example.mentormenteemanagement.model.Mentee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface MenteeRepository extends JpaRepository<Mentee, Long> {
    List<Mentee> findByNameContainingIgnoreCase(String name);
    List<Mentee> findByMentorIsNull();
    int countByMentorId(Long mentorId);
    List<Mentee> findByMentor_Id(Long mentorId);
    
    // New method: Find unassigned mentees by year
    List<Mentee> findByYearAndMentorIsNull(int year);
    Optional<Mentee> findByName(String name);
    List<Mentee> findByParent_Id(Long parentId);
}
