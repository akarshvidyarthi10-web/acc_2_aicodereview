package com.example.service;

public class UserService {

    private final AuthService authService = new AuthService();

    public void login(String token) {

        if (authService.validateToken(token)) {
            System.out.println("User Login Success");
        }
    }
}
