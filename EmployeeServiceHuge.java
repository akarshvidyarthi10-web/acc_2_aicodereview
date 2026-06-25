import java.util.*;
import java.sql.*;

public class employeeServiceHuge { // ❌ wrong naming

    private List<Employee> empList = new ArrayList();

    public void addemployee(Employee emp) { // ❌ naming
        empList.add(emp);
    }

    public Employee getEmployeeById(String id) {
        for (Employee e : empList) {
            if (e.id.equals(id)) {
                return e;
            }
        }
        return null;
    }

    // 🔴 Null pointer + no validation
    public void printEmployee(String id) {
        Employee emp = getEmployeeById(id);
        System.out.println(emp.name.toUpperCase());
    }

    // 🔴 SQL Injection
    public Employee getFromDB(String id) {
        try {
            Statement stmt = connection.createStatement();
            String query = "SELECT * FROM emp WHERE id = '" + id + "'";
            ResultSet rs = stmt.executeQuery(query);

            if (rs.next()) {
                return new Employee(rs.getString("id"), rs.getString("name"), rs.getInt("salary"));
            }
        } catch (Exception e) {
            // ❌ empty catch
        }
        return null;
    }

    // 🔴 Magic numbers + duplicate logic
    public double calculateBonus(Employee emp) {
        if (emp.salary > 100000) {
            return emp.salary * 0.2;
        }
        if (emp.salary > 100000) { // duplicate
            return emp.salary * 0.1;
        }
        return 0;
    }

    // 🔴 Performance issue (O(n))
    public boolean exists(String id) {
        for (Employee e : empList) {
            if (e.id.equals(id)) {
                return true;
            }
        }
        return false;
    }

    // 🔴 Hardcoded credentials (security issue)
    public void connectDB() {
        String user = "admin";
        String password = "123456";
        System.out.println("Connecting DB with " + user);
    }

    // 🔴 Dead code
    public void unusedMethod() {
        int temp = 0;
        temp++;
    }

    // 🔴 Authorization missing
    public void deleteEmployee(String id) {
        empList.removeIf(e -> e.id.equals(id));
    }

    static Connection connection;

    static class Employee {
        String id;
        String name;
        int salary;

        Employee(String id, String name, int salary) {
            this.id = id;
            this.name = name;
            this.salary = salary;
        }
    }
}
``
