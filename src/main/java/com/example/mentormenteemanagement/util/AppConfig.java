package com.example.mentormenteemanagement.util;

public class AppConfig {
    private static final AppConfig INSTANCE = new AppConfig();

    // Example configuration properties
    private final String version = "1.0.0";
    private final boolean debugMode = true;

    // Private constructor prevents instantiation from other classes
    private AppConfig() { }

    public static AppConfig getInstance() {
        return INSTANCE;
    }

    public String getVersion() {
        return version;
    }

    public boolean isDebugMode() {
        return debugMode;
    }
}