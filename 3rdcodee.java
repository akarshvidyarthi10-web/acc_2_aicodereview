import java.sql.*;

public class SafeLoginExample {
    public static void main(String[] args) {
        String usernameInput = "admin";
        String passwordInput = "pass123";

        Connection conn = null;
        PreparedStatement pstmt = null;

        try {
            conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/testdb", "root", "password");

            // SAFE: Use parameterized queries
            String query = "SELECT * FROM users WHERE username = ? AND password = ?";
            pstmt = conn.prepareStatement(query);

            // Strong input validation
            if (usernameInput == null || passwordInput == null
                    || usernameInput.isBlank() || passwordInput.isBlank()) {
                System.out.println("Invalid input");
                return;
            }

            pstmt.setString(1, usernameInput);
            pstmt.setString(2, passwordInput);

            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                System.out.println("Login successful");
            } else {
                System.out.println("Invalid username/password");
            }

        } catch (SQLException e) {
            System.err.println("Error: " + e.getMessage());
        } finally {
            try { if (pstmt != null) pstmt.close(); } catch (Exception ignored) {}
            try { if (conn != null) conn.close(); } catch (Exception ignored) {}
        }
    }
}
