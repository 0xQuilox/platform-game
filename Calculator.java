import java.util.Scanner;

public class Calculator {

    // Scanner is Java's way of reading user input — like Python's input()
    // We create ONE scanner and share it across all methods (DRY principle)
    static Scanner scanner = new Scanner(System.in);


    // ── OPERATION FUNCTIONS ──────────────────────────────────
    // Same as Python — each function does ONE job.
    // 'static double' means: this method belongs to the class (not an
    // object) and returns a decimal number.

    static double add(double a, double b) {
        return a + b;
    }

    static double subtract(double a, double b) {
        return a - b;
    }

    static double multiply(double a, double b) {
        return a * b;
    }

    // Returns Double (capital D = object wrapper), NOT double (primitive).
    // This lets us return null on division by zero — just like Python's None.
    // A primitive double cannot be null; a Double object can.
    static Double divide(double a, double b) {
        if (b == 0) {
            return null;    // null in Java == None in Python
        }
        return a / b;
    }


    // ── INPUT FUNCTIONS ──────────────────────────────────────

    static double getNumber(String prompt) {
        //
        // Keeps asking until the user enters a valid number.
        // The validation loop logic is IDENTICAL to Python.
        //
        // Python:                         Java:
        //   try:                            try {
        //     value = float(input())          value = Double.parseDouble(...)
        //   except ValueError:              } catch (NumberFormatException e) {
        //     print("invalid")                System.out.println("invalid")
        //                                   }
        //
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim();

            try {
                return Double.parseDouble(input);
            } catch (NumberFormatException e) {
                System.out.println("  ⚠  That's not a valid number. Please try again.\n");
            }
        }
    }

    static String getOperation() {
        //
        // Displays the menu and returns the user's valid choice.
        // 'while (true)' is the same infinite loop as Python's 'while True:'
        //
        System.out.println();
        System.out.println("  Select an operation:");
        System.out.println("  ┌─────────────────────┐");
        System.out.println("  │  1.  Addition   (+) │");
        System.out.println("  │  2.  Subtraction(-) │");
        System.out.println("  │  3.  Multiply   (*) │");
        System.out.println("  │  4.  Divide     (/) │");
        System.out.println("  │  5.  Quit           │");
        System.out.println("  └─────────────────────┘");

        String[] validChoices = {"1", "2", "3", "4", "5"};

        while (true) {
            System.out.print("  Enter choice (1-5): ");
            String choice = scanner.nextLine().trim();

            // TEACHING POINT: Java has no 'in' keyword like Python.
            // Python:  if choice in valid_choices
            // Java:    loop through the array and check each one
            for (String valid : validChoices) {
                if (choice.equals(valid)) {
                    return choice;
                    // IMPORTANT: Always use .equals() to compare Strings in Java.
                    // Using == compares memory addresses, not the actual text content —
                    // a very common Java bug for beginners coming from Python.
                }
            }
            System.out.println("  ⚠  Please enter a number between 1 and 5.\n");
        }
    }

    static void displayResult(double a, String operator, double b, double result) {
        // 'void' means this method returns nothing —
        // same as a Python function with no return statement.
        System.out.println();
        System.out.println("  ┌─────────────────────────────┐");
        System.out.println("  │  " + fmt(a) + " " + operator + " " + fmt(b) + " = " + fmt(result));
        System.out.println("  └─────────────────────────────┘");
    }

    // Helper: show whole numbers without a decimal point (5.0 → "5")
    // This mirrors the fmt() helper inside display_result() in Python.
    static String fmt(double n) {
        if (n == Math.floor(n) && !Double.isInfinite(n)) {
            return String.valueOf((long) n);
        }
        return String.valueOf(Math.round(n * 1_000_000.0) / 1_000_000.0);
    }


    // ── MAIN PROGRAM ─────────────────────────────────────────
    //
    // In Java, execution ALWAYS starts from main().
    // This is Java's equivalent of Python's:
    //   if __name__ == "__main__":
    //       main()
    //
    // Signature breakdown:
    //   public       → accessible from anywhere
    //   static       → belongs to the class, not an instance/object
    //   void         → returns nothing
    //   String[] args → command-line arguments (unused here)

    public static void main(String[] args) {

        System.out.println();
        System.out.println("  ╔═══════════════════════════╗");
        System.out.println("  ║     CLI CALCULATOR        ║");
        System.out.println("  ║   Phase 1 — Java          ║");
        System.out.println("  ╚═══════════════════════════╝");

        // Same while(true) loop as Python — runs until user picks Quit
        while (true) {

            String choice = getOperation();

            // Exit
            // TEACHING POINT: .equals("5") not == "5"
            if (choice.equals("5")) {
                System.out.println();
                System.out.println("  Goodbye! Keep coding. 👋");
                System.out.println();
                break;
            }

            // Get the two numbers — same as Python
            double a = getNumber("\n  Enter first number:  ");
            double b = getNumber("  Enter second number: ");

            // TEACHING POINT: switch/case in Java works like if/elif in Python.
            // Python:           Java:
            //   if choice=="1"    case "1":
            //   elif choice=="2"  case "2":
            //   elif choice=="3"  case "3":
            //   elif choice=="4"  case "4":
            // The 'break' after each case stops it from falling into the next one.
            switch (choice) {
                case "1":
                    displayResult(a, "+", b, add(a, b));
                    break;

                case "2":
                    displayResult(a, "-", b, subtract(a, b));
                    break;

                case "3":
                    displayResult(a, "*", b, multiply(a, b));
                    break;

                case "4":
                    Double result = divide(a, b);
                    if (result == null) {
                        System.out.println();
                        System.out.println("  ⚠  Error: You can't divide by zero!");
                    } else {
                        displayResult(a, "/", b, result);
                    }
                    break;
            }

            // Ask to continue
            System.out.println();
            System.out.print("  Calculate again? (y/n): ");
            String again = scanner.nextLine().trim().toLowerCase();

            // TEACHING POINT: !again.equals("y") is the same as: again != "y" in Python
            // The ! operator means NOT in Java (same as 'not' in Python)
            if (!again.equals("y")) {
                System.out.println();
                System.out.println("  Goodbye! Keep coding. 👋");
                System.out.println();
                break;
            }
        }

        scanner.close();    // always close the Scanner when you're done with it
    }
}
