// Vulnerable: storing plain-text passwords
String username = request.getParameter("username");
String password = request.getParameter("password");

// Compare directly with DB-stored plain text
if (dbPassword.equals(password)) {
    loginUser(username);
}
