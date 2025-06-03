"""
Siau, Jacob 

DSC510-T303 Week 2 Assignment 2.1

Description: This script defines a program that does the following:
1. Welcomes the user.
2. Asks the user for their company name.
3. Asks the user for the number of feet of fiber optic cable they need.
4. Calculates the cost of this length of fiber optic cable by multiplying by $0.95 per foot.
5. Displays a receipt with the company name, number of feet of fiber optic cable, and the total cost.
"""

if __name__ == "__main__":
    print("Welcome to Jacob Siau's fiber optic cable installation service!")

    # get user input for company name and feet of cable
    company_name = input("Please enter your company name: ")

    feet_of_cable = -1
    while feet_of_cable < 0:
        try:
            feet_of_cable = float(input("Please enter the amount of fiber optic cable you need (in feet): "))
        except ValueError:
            print(f"Invalid input! Please enter a numeric value for the feet of cable.")

    # Calculate the total cost
    cost_per_foot = 0.95 # Cost per foot of fiber optic cable per the assignment
    total_cost = feet_of_cable * cost_per_foot

    print("\nReceipt:")
    print(f"Company name: {company_name}")
    print(f"Feet of fiber optic cable installed: {feet_of_cable} feet")
    print(f"Total cost: ${total_cost:.2f}")