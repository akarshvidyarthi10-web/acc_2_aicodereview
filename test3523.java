public class Test {

    public static void main(String[] args) {
        
        int a = 10;
        int b = 0;

        // Potential bug: division by zero
        int result = a / b;

        System.out.println("Result is: " + result);

        // Bad practice: unused variable
        int unused = 100;
    }
}
``
