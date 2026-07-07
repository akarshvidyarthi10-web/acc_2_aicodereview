public class ErrorTest {
    public static void main(String[] args) {
        // Intentional errors included below

        int number = "five"; // ❌ Type mismatch: assigning String to int

        System.out.println("The number is: " + number);

        // ❌ Misspelled method name
        prinln("This line will not compile");

        // ❌ Array index out of bounds
        int[] arr = new int[3];
        arr[5] = 10;

        // ❌ Missing semicolon
        String message = "Hello World"
        
        System.out.println(message);
    }
}
