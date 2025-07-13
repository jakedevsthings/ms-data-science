"""
Siau, Jacob 

DSC510-T303 Week 6 Assignment 6.1

Description: This script defines a program that does the following:
1. Populates a list of temperatures from user input using a sentinel value and while loop.
2. Determine the number of temperatures entered by the user and stored in the list.
3. Determine the highest temperature in the list.
4. Determine the lowest temperature in the list.
"""

def main():
    """
    Main function that runs the program.
    """
    temperatures = []
    while True:
        temp = input("Enter a temperature (or 'done' to finish): ")
        if temp == 'done':
            break
        try:
            temp = float(temp)
            temperatures.append(temp)
        except ValueError:
            print("Invalid input! Please enter a valid temperature.")

    if not temperatures:
        print("No temperatures were entered.")
    else:
        print(f"Number of temperatures entered: {len(temperatures)}")
        print(f"Highest temperature: {max(temperatures)}")
        print(f"Lowest temperature: {min(temperatures)}")


if __name__ == "__main__":
    main()
