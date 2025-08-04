"""
Siau, Jacob 

DSC510-T303 Week 9 Assignment 9.1

Description: This script defines a program that does the following:
1. Retrieves a list of categories from the Chuck Norris Facts API.
2. Allows the user to select a category for a random fact.
3. Retrieves a random fact from the selected category.
4. Prints the fact to the console.
5. Allows the user to select another category for a random fact.
6. Repeats steps 3-5 until the user quits.
"""
import requests
import json
import os


CATEGORIES_ENDPOINT = "https://api.chucknorris.io/jokes/categories"
FACTS_ENDPOINT = "https://api.chucknorris.io/jokes/random"
    
def pretty_print(dict_data):
    """
    Pretty print the dictionary data.
    """
    print(json.dumps(dict_data, indent=4))

def display_categories(categories_dict):
    """
    Display categories in a clean numbered vertical list.
    """
    print("\nAvailable Categories:")
    print("-" * 20)
    for number, category in categories_dict.items():
        print(f"{number}. {category.title()}")
    print("0. Quit")
    print("-" * 20)

def clear_screen():
    """
    Clear the console screen for better UX.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """
    This program will retrieve a random Chuck Norris fact from the Chuck Norris Facts API.
    It will allow the user to select a category for a random fact.
    It will then retrieve a random fact from the selected category.
    It will print the fact to the console.
    It will allow the user to select another category for a random fact.
    It will repeat steps 3-5 until the user quits.
    """

    clear_screen()
    print("Welcome to the Chuck Norris Facts Retriever by Jacob Siau.")
    print("This program will retrieve a random Chuck Norris fact from the Chuck Norris Facts API.")

    # Get the categories
    try:
        categories_response = requests.get(CATEGORIES_ENDPOINT)
        if categories_response.status_code == 200:
            categories = categories_response.json()
            # make numbered options for the categories  
            categories_options = {index + 1: category for index, category in enumerate(categories)} 
            display_categories(categories_options)
        else:
            print(f"Error: {categories_response.status_code}")
            print(categories_response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting categories: {e}")
        return None

    # User selects a category for a random fact
    while True:
        try:
            category_number = int(input("\nEnter a number for a category for a random fact (or 0 to quit): "))
            if category_number == 0:
                clear_screen()
                print("Thank you for using Chuck Norris Facts Retriever!")
                print("Program terminated by user.")
                return None
            elif category_number in categories_options:
                category = categories_options[category_number]
                print(f"\nYou selected category: '{category.title()}'")
                print("=" * 50)
                try:
                    fact_response = requests.get(f"{FACTS_ENDPOINT}?category={category}")
                    if fact_response.status_code == 200:
                        fact = fact_response.json()
                        print(f"\n{fact['value']}")
                        print("=" * 50)
                        input("\nPress Enter to continue...")
                        clear_screen()
                        print("Chuck Norris Facts Retriever")
                        display_categories(categories_options)
                    else:
                        print(f"Error from fact endpoint, endpoint returned: {fact_response.status_code}")
                        print(fact_response.text)
                except requests.exceptions.RequestException as e:
                    print(f"Error making request for random fact from category {category}: {e}")
                    return None
            else:
                print("Invalid category. Please enter a number from the list of categories to get a random fact from that category.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            return None

if __name__ == "__main__":
    main()