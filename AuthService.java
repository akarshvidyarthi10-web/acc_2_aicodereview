package com.example.service;

public class AuthService {

    public boolean validateToken(String token) {
        return token != null && !token.isEmpty();
    }
}
