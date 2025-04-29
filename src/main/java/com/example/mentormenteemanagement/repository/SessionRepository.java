package com.example.mentormenteemanagement.repository;

import com.example.mentormenteemanagement.model.Session;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface SessionRepository extends JpaRepository<Session, Long> {
    int countByMentee_Id(Long menteeId);

    // existing mentor methods…
    List<Session> findByMentor_Id(Long mentorId);
    List<Session> findByMentor_IdAndCompletedTrue(Long mentorId);

    // << NEW >> for mentee:
    List<Session> findByMentee_IdAndCompletedTrue(Long menteeId);
    List<Session> findByMentee_IdAndCompletedFalseAndScheduledTimeAfter(
        Long menteeId, LocalDateTime now);
}
