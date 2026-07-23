package com.example.service;

public class AdminService {

    private final AuthService authService = new AuthService();

    public void authenticate(String token) {

        if (authService.validateToken(token)) {
            System.out.println("Admin Auth Success");
        }
    }
}
