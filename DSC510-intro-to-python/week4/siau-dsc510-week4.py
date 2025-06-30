"""
Siau, Jacob 

DSC510-T303 Week 4 Assignment 4.1

Description: This script defines a program that does the following:
1. Welcomes the user.
2. Asks the user for their company name.
3. Asks the user for the number of feet of fiber optic cable they need.
4. Calculates the cost using bulk discount pricing:
   - 0-100 feet: $0.95 per foot
   - 101-250 feet: $0.85 per foot
   - 251-500 feet: $0.75 per foot
   - Over 500 feet: $0.55 per foot
5. Displays a receipt with the company name, number of feet of fiber optic cable, cost per foot, and the total cost.
"""

def calculate_cost(feet_of_cable, cost_per_foot):
    """
    Calculates the total cost of the fiber optic cable installation.
    Args:
        feet_of_cable (float): The number of feet of fiber optic cable to be installed.
        cost_per_foot (float): The cost per foot of fiber optic cable.
    Returns:
        float: The total cost of the fiber optic cable installation.
    """
    return feet_of_cable * cost_per_foot

def main():
    print("Welcome to Jacob Siau's fiber optic cable installation service 2.0, now with bulk discounts!")

    # get user input for company name and feet of cable
    company_name = input("Please enter your company name: ")

    # get user input for feet of cable
    # validate input to ensure it is a positive number
    feet_of_cable = -1
    while feet_of_cable < 0:
        try:
            feet_of_cable = float(input("Please enter the amount of fiber optic cable you need (in feet): "))
        except ValueError:
            print("Invalid input! Please enter a numeric value for the feet of cable.")

    # Calculate the cost per foot based on the number of feet of cable
    if feet_of_cable <= 100:
        bulk_discount_level = "0-100 feet"
        cost_per_foot = 0.95
    elif feet_of_cable <= 250:
        bulk_discount_level = "100-250 feet"
        cost_per_foot = 0.85
    elif feet_of_cable <= 500:
        bulk_discount_level = "250-500 feet"
        cost_per_foot = 0.75
    else:
        bulk_discount_level = "500+ feet"
        cost_per_foot = 0.55
    
    # Calculate the total cost
    total_cost = calculate_cost(feet_of_cable, cost_per_foot)

    print("\nReceipt:")
    print(f"Company name: {company_name}")
    print(f"Feet of fiber optic cable installed: {feet_of_cable} feet")
    print(f"Cost per foot ({bulk_discount_level}): ${cost_per_foot:.2f}")
    print(f"Total cost: ${total_cost:.2f}")

if __name__ == "__main__":
    main()