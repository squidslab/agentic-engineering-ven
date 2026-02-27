# Code Smell Analysis Report: `Pub.java`

## Overview
This report summarizes the code smells identified in the `computeCost` method and related methods within the `Pub` class in `src\main\java\nerdschool\bar\Pub.java`. The findings are grouped by severity and type, with actionable refactoring strategies provided for each issue.

---

## High Severity Issues

### 1. **Inappropriate Use of `==` for String Comparison**
- **Problematic Code**:  
  ```java
  if (drink == GT || drink == BACARDI_SPECIAL)
  ```
- **Explanation**:  
  Using `==` to compare `String` objects checks for reference equality, not value equality. This can lead to unexpected behavior, especially with string literals that are not interned.
- **Refactoring Strategy**:  
  Replace `==` with the `.equals()` method. If `GT` and `BACARDI_SPECIAL` are constants, ensure they are declared as `static final String` and use `.equals()` for comparison.  
  **Example**:  
  ```java
  if (drink.equals(GT) || drink.equals(BACARDI_SPECIAL))
  ```

---

## Medium Severity Issues

### 2. **Hardcoded Values in Private Methods**
- **Problematic Code**:  
  ```java
  private int ingredient1() { return 65; }
  private int ingredient2() { return 70; }
  // ... (similar for ingredient3 to ingredient6)
  ```
- **Explanation**:  
  Hardcoded values for ingredient prices are scattered across multiple private methods, making the codebase difficult to maintain and adjust without modifying the source code.
- **Refactoring Strategy**:  
  Externalize these values into a `Constants` class or a configuration file (e.g., `application.properties`).  
  **Example**:  
  ```java
  public class DrinkConstants {
      public static final int INGREDIENT_1_PRICE = 65;
      public static final int INGREDIENT_2_PRICE = 70;
      // ... (other ingredients)
  }
  ```
  Replace method calls with direct references to the constants.

---

## Low Severity Issues

### 3. **Inefficient Integer Division for Discount Calculation**
- **Problematic Code**:  
  ```java
  price = price - price / 10;
  ```
- **Explanation**:  
  Using integer division (`price / 10`) truncates the decimal part, leading to incorrect discount calculations (e.g., a 10% discount on 105 would result in 94.5 being truncated to 94).
- **Refactoring Strategy**:  
  Replace integer division with floating-point arithmetic or use a percentage-based calculation.  
  **Example**:  
  ```java
  price = (int) (price * 0.9); // 10% discount using floating-point
  ```

---

## High Severity Issues

### 4. **Generic Exception Handling**
- **Problematic Code**:  
  ```java
  throw new RuntimeException("Too many drinks, max 2.");
  ```
- **Explanation**:  
  Throwing generic `RuntimeException` without specific error types or messages reduces clarity and makes error handling less precise.
- **Refactoring Strategy**:  
  Use specific exception types (e.g., `IllegalArgumentException`) or define custom exceptions for business rules.  
  **Example**:  
  ```java
  throw new IllegalArgumentException("Maximum of 2 drinks allowed.");
  ```

---

## High Severity Issues

### 5. **Violation of Single Responsibility Principle**
- **Problematic Code**:  
  The `computeCost` method handles multiple responsibilities:  
  - Input validation  
  - Price calculation  
  - Discount application  
  - Constraint enforcement  
- **Explanation**:  
  This violates the Single Responsibility Principle (SRP), making the method harder to test, maintain, and understand.
- **Refactoring Strategy**:  
  Break `computeCost` into smaller, focused methods:  
  - `validateDrinkInput()`  
  - `calculateBasePrice()`  
  - `applyDiscounts()`  
  - `enforceConstraints()`  
  **Example**:  
  ```java
  private void validateDrinkInput(String drink) { ... }
  private int calculateBasePrice(String drink) { ... }
  ```

---

## Summary of Recommendations
| Code Smell                          | Severity   | Refactoring Strategy                                  |
|-----------------------------------|------------|------------------------------------------------------|
| `==` for String comparison        | High       | Use `.equals()` and ensure string literals are interned |
| Hardcoded ingredient prices       | Medium     | Externalize values into a `Constants` class or config file |
| Integer division for discounts    | Low        | Use floating-point arithmetic or `BigDecimal`        |
| Generic `RuntimeException`        | High       | Replace with specific exceptions or custom exceptions |
| SRP violation in `computeCost`    | High       | Decompose into smaller, single-responsibility methods |

---

## Conclusion
The `Pub` class requires significant refactoring to address critical issues such as incorrect string comparison, hardcoded values, and SRP violations. Implementing the suggested strategies will improve maintainability, reduce bugs, and align the code with best practices. Prioritize high-severity issues (e.g., SRP and string comparison) first, followed by medium and low-severity improvements.