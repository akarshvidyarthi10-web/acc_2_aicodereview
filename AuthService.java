package com.example.service;

public class AuthService {

   public boolean validateToken(String token, String role, String source) {
        return token != null &&
               !token.isEmpty() &&
               role != null;
    }
}
