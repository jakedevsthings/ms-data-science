"""
Siau, Jacob 

DSC510-T303 Week 5 Assignment 5.1

Description: This script defines a program that does the following:
1. Calculates the average of a list of numbers.
2. Performs a mathematical calculation based on the user's input.
3. Displays the result of the calculation.
"""


def calculate_average():
    """
    Calculates the average of a user-defined number of numbers.
    Returns:
        The average of the numbers.
    """
    try:
        count_of_numbers = int(input("How many numbers do you want to input? "))
    except ValueError:
        print("Invalid input! Please enter a valid integer.")
        return 0
        
    if count_of_numbers <= 0:
        print("Invalid input! Please enter a positive number.")
        return 0
    
    sum_of_numbers = 0
    
    for i in range(count_of_numbers):
        while True:
            try:
                number = float(input(f"Enter number {i + 1}: "))
                sum_of_numbers += number
                break
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
    
    if count_of_numbers == 0:
        return 0
    return sum_of_numbers / count_of_numbers


def perform_calculation(operation):
    """
    Performs a calculation based on user input.
    Args:
        operation: the operation to perform
        possible operations: +, -, *, /
    Returns:
        The result of the calculation.
    Raises:
        ValueError: If the user enters an invalid operation.
        ZeroDivisionError: If the user tries to divide by zero.
    """
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    except ValueError:
        raise ValueError("Invalid input! Please enter numeric values.")

    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return num1 / num2
    else:
        raise ValueError("Invalid operation. Please enter +, -, *, or /.")

def main():
    """
    Main function that runs the program.
    Contains a while loop to allow multiple calculations and proper error handling.
    """
    print("Welcome to Jacob Siau's Python Calculator!")
    print("=" * 50)
    
    while True:
        try:
            print("\nAvailable operations:")
            print("1. Addition (+)")
            print("2. Subtraction (-)")
            print("3. Multiplication (*)")
            print("4. Division (/)")
            print("5. Average calculation")
            print("6. Exit")
            
            choice = input("\nPlease select an operation (1-6): ").strip()
            
            if choice == "6":
                print("Thank you for using Jacob Siau's Python Calculator!")
                break
            elif choice == "5":
                # Calculate average
                try:
                    average_result = calculate_average()
                    if average_result != 0:
                        print(f"\nThe average of the numbers is: {average_result:.2f}")
                    else:
                        print("\nNo valid numbers were entered to calculate average.")
                except ValueError as e:
                    print(f"Error calculating average: {e}")
            elif choice in ["1", "2", "3", "4"]:
                # Perform calculation
                operation_map = {
                    "1": "+",
                    "2": "-", 
                    "3": "*",
                    "4": "/"
                }
                operation = operation_map[choice]
                
                try:
                    result = perform_calculation(operation)
                    operation_name_map = {
                        "+": "addition",
                        "-": "subtraction", 
                        "*": "multiplication",
                        "/": "division"
                    }
                    operation_name = operation_name_map[operation]
                    print(f"\nThe result of {operation_name} is: {result:.2f}")
                except ValueError as e:
                    print(f"Error performing calculation: {e}")
                except ZeroDivisionError:
                    print("Error: Cannot divide by zero.")
            else:
                print("Invalid choice! Please enter a number between 1 and 6.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
