import java.sql.*;

public class VulnerableLoginExample {
    public static void main(String[] args) {
        String userInputUsername = "' OR '1'='1";  // Attacker input
        String userInputPassword = "anything";

        Connection conn = null;
        Statement stmt = null;

        try {
            conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/testdb", "root", "password");

            stmt = conn.createStatement();

            // VULNERABLE: Direct string concatenation
            String query = "SELECT * FROM users WHERE username='" 
                            + userInputUsername + "' AND password='" 
                            + userInputPassword + "'";

            ResultSet rs = stmt.executeQuery(query);

            if (rs.next()) {
                System.out.println("Logged in (due to SQL injection!)");
            } else {
                System.out.println("Login failed");
            }

        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        } finally {
            try { if (stmt != null) stmt.close(); } catch (Exception ignored) {}
            try { if (conn != null) conn.close(); } catch (Exception ignored) {}
        }
    }
}
