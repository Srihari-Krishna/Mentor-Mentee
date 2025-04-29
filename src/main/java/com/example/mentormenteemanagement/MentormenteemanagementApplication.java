package com.example.mentormenteemanagement;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class MentormenteemanagementApplication {

	public static void main(String[] args) {
		SpringApplication.run(MentormenteemanagementApplication.class, args);
	}

}
