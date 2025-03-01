import java.util.List;
import java.util.ArrayList;
import com.example.utils.Helper;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Java Coding Standards

// 1. Formatting Rules
// - Indentation: Use 4 spaces per indentation level. Do not use tabs.
// - Line Length: Limit all lines to a maximum of 100 characters.
// - Braces: Place opening brace on the same line as the declaration.
// - Spacing: Use a single space before opening braces and after commas.

public class Example {
    public void exampleMethod(int a, int b) {
        if (a > b) {
            System.out.println("a is greater than b");
        } else {
            System.out.println("a is not greater than b");
        }
    }
}

// 2. Naming Conventions
// - Class Names: Use PascalCase (e.g., MyClass, UserManager).
// - Method Names: Use camelCase (e.g., calculateTotal, processRequest).
// - Variable Names: Use camelCase (e.g., userName, orderAmount).
// - Constant Names: Use UPPER_CASE with underscores (e.g., MAX_RETRIES, DEFAULT_TIMEOUT).
// - Package Names: Use lowercase with dots separating words (e.g., com.example.utils).

public class UserManager {
    private String userName;
    private static final int MAX_RETRIES = 3;

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }
}

// 3. Import Guidelines
// - Import only necessary classes. Avoid wildcard imports.
// - Organize imports in the order: standard library, third-party libraries, project-specific imports.


// 4. Code Structure
// - Keep methods short (ideally under 50 lines). Each method should have a single responsibility.
// - Use meaningful method and variable names that reflect their purpose.
// - Use proper access modifiers: private for internal logic, public for exposed methods.
// - Group related methods and constants logically inside classes.

public class OrderProcessor {
    private List<Order> orders;

    public OrderProcessor() {
        this.orders = new ArrayList<>();
    }

    public void processOrders() {
        for (Order order : orders) {
            processOrder(order);
        }
    }

    private void processOrder(Order order) {
        // Process the order
    }
}

// 6. Exception Handling
// Catch only specific exceptions. Avoid catching generic Exception or Throwable.
// Always log exceptions with meaningful messages.
// Use try-with-resources for handling AutoCloseable resources.

public class FileProcessor {
    public void processFile(String filePath) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }
}

// 7. Readability and Best Practices
// Avoid magic numbers. Use named constants instead.
// Use StringBuilder for string concatenations inside loops.
// Use Optional to handle null values where appropriate.
// Follow SOLID principles to ensure maintainable and scalable code.

public class ReportGenerator {
    private static final int MAX_ENTRIES = 100;

    public String generateReport(List<String> entries) {
        StringBuilder report = new StringBuilder();
        for (String entry : entries) {
            report.append(entry).append("\n");
        }
        return report.toString();
    }

    public Optional<String> findEntry(List<String> entries, String keyword) {
        return entries.stream().filter(entry -> entry.contains(keyword)).findFirst();
    }
}

// 8. Testing Standards
// Write unit tests for all public methods using JUnit.
// Test class names should follow the naming pattern ClassNameTest (e.g., CalculatorTest).
// Use descriptive test method names (e.g., testAdditionWithPositiveNumbers).


public class CalculatorTest {
    @Test
    public void testAdditionWithPositiveNumbers() {
        Calculator calculator = new Calculator();
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    public void testAdditionWithNegativeNumbers() {
        Calculator calculator = new Calculator();
        assertEquals(-1, calculator.add(-2, 1));
    }
}
