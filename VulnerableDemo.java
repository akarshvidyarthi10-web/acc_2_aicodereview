import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;

public class VulnerableDemo extends HttpServlet {

    // 🔴 Missing CSRF protection + insecure POST handling
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String toAccount = request.getParameter("toAccount");
        String amount = request.getParameter("amount");

        // 🔴 No validation / authorization
        transferMoney(toAccount, amount);
    }

    // 🔴 Insecure Direct Object Reference (IDOR)
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String accountId = request.getParameter("accountId");

        // 🔴 No ownership check
        Account account = accountService.getAccount(accountId);

        response.getWriter().println("Account: " + account);
    }

    // 🔴 Path Traversal vulnerability
    protected void forwardPage(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String page = request.getParameter("page");

        // 🔴 User-controlled path
        RequestDispatcher rd = request.getRequestDispatcher("/pages/" + page);
        rd.forward(request, response);
    }

    // 🔴 SQL Injection
    public Account getAccountFromDB(String id) {
        try {
            String query = "SELECT * FROM accounts WHERE id = '" + id + "'";

            // Assume connection exists
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery(query);

            if (rs.next()) {
                return new Account(rs.getString("id"), rs.getString("name"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    // Dummy methods
    private void transferMoney(String toAccount, String amount) {
        System.out.println("Transferred " + amount + " to " + toAccount);
    }

    private static class Account {
        String id;
        String name;

        Account(String id, String name) {
            this.id = id;
            this.name = name;
        }

        public String toString() {
            return id + ":" + name;
        }
    }

    // Mock objects (for compilation simulation)
    static java.sql.Connection connection;
    static AccountService accountService;

    static class AccountService {
        public Account getAccount(String id) {
            return new Account(id, "DemoUser");
        }
    }
}
