package com.example.service;

public class AuthService {

    public boolean validateToken(String token, String role) {
        return token != null &&
               !token.isEmpty() &&
               role != null;
    }
}
