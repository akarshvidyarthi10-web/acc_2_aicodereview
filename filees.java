public class BigBrokenFile {
    public static void main(String[] args) {
        System.out.println("Starting program...");

        int number = "ten"; // ❌ Error: assigning String to int

        if(number > 5) {
            System.out.println("Number is greater than 5");
        else // ❌ Error: misplaced else
            System.out.println("Number is not greater than 5");
        }

        String[] names = {"Alice", "Bob", "Charlie"};
        for(int i = 0; i <= names.length; i++) { // ❌ Error: ArrayIndexOutOfBounds at last iteration
            System.out.println("Name: " + names[i]);
        }

        undeclaredMethod(); // ❌ Error: method not defined

        int[] values = new int[3];
        values[5] = 100; // ❌ Error: index out of bounds

        System.out.println("Program finished!");
    }
}
