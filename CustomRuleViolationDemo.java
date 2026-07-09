public class badCustomRuleDemo { // ❌ Naming violation: class should be PascalCase

    private String dbUser = "admin";          // ❌ Hardcoded credential
    private String dbPassword = "password123"; // ❌ Hardcoded credential

    public void processdata(String userRole, int amount, boolean isActive) { // ❌ Method naming violation

        // TODO temporary workaround - remove later
        // ❌ Temporary workaround marker

        try {
            if (userRole != null) {
                if (userRole.equals("ADMIN")) {
                    if (isActive) {
                        if (amount > 0) { // ❌ Deep nesting more than 3 levels
                            System.out.println("Processing admin transaction");
                            System.out.println("Amount: " + amount);
                        } else {
                            System.out.println("Invalid amount");
                        }
                    } else {
                        System.out.println("Inactive user");
                    }
                } else {
                    System.out.println("User is not admin");
                }
            } else {
                System.out.println("User role is null");
            }
        } catch (Exception e) {
            // ❌ Empty catch block
        }

        // ❌ Duplicate logic starts
        if (amount > 1000) {
            System.out.println("High value transaction");
        }

        if (amount > 1000) {
            System.out.println("High value transaction");
        }
        // ❌ Duplicate logic ends

        // Extra lines to violate Method Length Rule > 50 lines
        System.out.println("Step 1");
        System.out.println("Step 2");
        System.out.println("Step 3");
        System.out.println("Step 4");
        System.out.println("Step 5");
        System.out.println("Step 6");
        System.out.println("Step 7");
        System.out.println("Step 8");
        System.out.println("Step 9");
        System.out.println("Step 10");
        System.out.println("Step 11");
        System.out.println("Step 12");
        System.out.println("Step 13");
        System.out.println("Step 14");
        System.out.println("Step 15");
        System.out.println("Step 16");
        System.out.println("Step 17");
        System.out.println("Step 18");
        System.out.println("Step 19");
        System.out.println("Step 20");
        System.out.println("Step 21");
        System.out.println("Step 22");
        System.out.println("Step 23");
        System.out.println("Step 24");
        System.out.println("Step 25");
        System.out.println("Step 26");
        System.out.println("Step 27");
        System.out.println("Step 28");
        System.out.println("Step 29");
        System.out.println("Step 30");
    }

    public void connectdb() { // ❌ Naming violation
        System.out.println("Connecting with user: " + dbUser);
        System.out.println("Password: " + dbPassword);
    }
}
