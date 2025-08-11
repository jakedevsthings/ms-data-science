"""
Siau, Jacob

DSC510-T303 Assignment 10.2 Final Project

Description:
    This script implements an application that interacts with the OpenWeatherMap API
    to retrieve weather data for a given city or zip code. The user can input a city or zip code,
    and the script will retrieve the weather data and display it in a readable format.
"""

import sys
import requests
from requests.exceptions import HTTPError, RequestException, Timeout


API_KEY = "INSERT API KEY HERE"
COUNTRY_CODE = "US"
GEO_ZIP_URL = "https://api.openweathermap.org/geo/1.0/zip"
GEO_DIRECT_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
HTTP_TIMEOUT = 10
US_STATE_ABBR = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC",
}


def input_menu_choice():
    """
    Ask the user which lookup to perform and return a valid menu option.
    """
    print("\nWeather Lookup")
    print("1) Search by ZIP code")
    print("2) Search by City + State (2-letter)")
    print("3) Quit")
    while True:
        user_input = input("Enter choice (1-3): ").strip()
        if user_input.isdigit():
            choice = int(user_input)
            if choice in (1, 2, 3):
                return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def input_units_choice():
    """
    Ask the user which units to use. Default to Fahrenheit.
    Returns OpenWeather 'units' parameter value: 'imperial', 'metric', or 'standard'.
    """
    print("\nSelect temperature units:")
    print("1) Fahrenheit (°F)")
    print("2) Celsius (°C)")
    print("3) Kelvin (K)")
    while True:
        selection = input("Enter choice (1-3) [default 1]: ").strip()
        if selection == "" or selection == "1":
            return "imperial"   # Fahrenheit
        if selection == "2":
            return "metric"     # Celsius
        if selection == "3":
            return "standard"   # Kelvin (not primary, but allowed)
        print("Invalid choice. Please enter 1, 2, or 3.")


def input_zip_code():
    """
    Prompt for a 5-digit ZIP code and validate it.
    """
    while True:
        zip_code = input("\nEnter 5-digit U.S. ZIP code: ").strip()
        if zip_code.isdigit() and len(zip_code) == 5:
            return zip_code
        print("Invalid ZIP. Please enter exactly 5 digits (e.g., 75201).")


def input_city_state():
    """
    Prompt for city and 2-letter state abbreviation and validate both.
    """
    while True:
        city = input("\nEnter city name (e.g., Bellevue): ").strip()
        # Check if the city name contains any digits
        if not city or any(ch.isdigit() for ch in city):
            print("Invalid city. Use alphabetic characters/spaces only.")
            continue

        state = input("Enter 2-letter state abbreviation (e.g., NE): ").strip().upper()
        if state in US_STATE_ABBR:
            return city, state

        print("Invalid state abbreviation. Example: TX, NE, CA, NY.")


def get_request(url, params):
    """
    Perform a GET request with robust error handling.
    
    Args:
        url (str): The URL to make the GET request to.
        params (dict): The parameters to pass to the GET request.

    Returns:
        requests.Response: The response from the GET request.

    Raises:
        Timeout: If the network timeout is exceeded.
        HTTPError: If the HTTP status code is 4xx or 5xx.
        RequestException: If there is a network error.
    """
    try:
        response = requests.get(url, params=params, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        return response
    except Timeout as exc:
        raise Timeout("Network timeout while contacting OpenWeather.") from exc
    except HTTPError as exc:
        # Try to include server-provided error detail, if any.
        details = ""
        try:
            details = f" Details: {response.text[:200]}..."
        except Exception:
            pass
        raise HTTPError(f"HTTP error {response.status_code} from OpenWeather.{details}") from exc
    except RequestException as exc:
        raise RequestException("Network error while contacting OpenWeather.") from exc


def geocode_by_zip(zip_code):
    """
    Geocode using ZIP code. Returns dict with name, state, lat, lon, country.
    
    Args:
        zip_code (str): The ZIP code to geocode.

    Returns:
        dict: A dictionary containing the geocoded location information, or None if not found.
    """
    params = {"zip": f"{zip_code},{COUNTRY_CODE}", "appid": API_KEY}
    try:
        resp = get_request(GEO_ZIP_URL, params)
        data = resp.json()
    except (RequestException, ValueError) as exc:
        print(f"Error during geocoding by ZIP: {exc}")
        return None

    # Expected fields: name, lat, lon, country, state (state may be present)
    required = ("name", "lat", "lon", "country")
    if not all(k in data for k in required):
        print("Unexpected ZIP geocode response format.")
        return None

    return {
        "name": data.get("name"),
        "state": data.get("state") or "",
        "lat": data["lat"],
        "lon": data["lon"],
        "country": data["country"],
    }


def geocode_by_city_state(city, state):
    """
    Geocode using city + state + country, limited to 1 best match.
    
    Args:
        city (str): The city to geocode.
        state (str): The state to geocode.

    Returns:
        dict: A dictionary containing the geocoded location information, or None if not found.
    """
    # Direct geocoding supports q="City,State,Country"
    query = f"{city},{state},{COUNTRY_CODE}"
    params = {"q": query, "limit": "1", "appid": API_KEY}
    try:
        resp = get_request(GEO_DIRECT_URL, params)
        data = resp.json()
    except (RequestException, ValueError) as exc:
        print(f"Error during geocoding by city/state: {exc}")
        return None

    if not isinstance(data, list) or not data:
        print("No matching city/state found. Please check spelling.")
        return None

    place = data[0]
    required = ("name", "lat", "lon", "country")
    if not all(k in place for k in required):
        print("Unexpected city/state geocode response format.")
        return None

    # OpenWeather direct geocode returns 'state' for US locations when available
    return {
        "name": place.get("name"),
        "state": place.get("state") or state,
        "lat": place["lat"],
        "lon": place["lon"],
        "country": place["country"],
    }


def fetch_current_weather(lat, lon, units):
    """
    Fetch current weather using lat/lon. Returns parsed JSON dict or None on error.

    Args:
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.
        units (str): The units to use for the weather data.

    Returns:
        dict: A dictionary containing the weather data, or None if not found.
    """
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": units}
    try:
        resp = get_request(WEATHER_URL, params)
        data = resp.json()
    except (RequestException, ValueError) as exc:
        print(f"Error fetching weather: {exc}")
        return None

    # Basic sanity check
    if "main" not in data or "weather" not in data or not data["weather"]:
        print("Unexpected weather response format.")
        return None

    return data


def unit_symbol(units):
    """
    Return a temperature unit symbol for the selected units.

    Args:
        units (str): The units to use for the weather data.

    Returns:
        str: The temperature unit symbol for the selected units.
    """
    return {"imperial": "°F", "metric": "°C", "standard": "K"}.get(units, "")


def format_weather_report(loc, wx, units):
    """
    Build a nice, readable string report of the weather.

    Args:
        loc (dict): The location information.
        wx (dict): The weather data.
        units (str): The units to use for the weather data.

    Returns:
        str: A nicely formatted string report of the weather.
    """
    u = unit_symbol(units)
    main = wx.get("main", {})
    clouds = wx.get("clouds", {})
    weather_list = wx.get("weather", [])
    description = weather_list[0].get("description", "").title() if weather_list else ""
    cloud_pct = clouds.get("all", "N/A")

    # Name preference: geocode name/state/country, fall back to weather name/country
    loc_str = f"{loc.get('name', 'Unknown')}, {loc.get('state', '').upper()} {loc.get('country', '')}".strip()
    # Replace double spaces with single spaces and strip any trailing commas
    loc_str = loc_str.replace(",  ", ", ").replace("  ", " ").strip(", ")

    lines = [
        "\n----------------------------------------",
        f"Weather for: {loc_str}",
        f"Conditions : {description or 'N/A'}",
        f"Current    : {main.get('temp', 'N/A')} {u}",
        f"High / Low : {main.get('temp_max', 'N/A')} {u} / {main.get('temp_min', 'N/A')} {u}",
        f"Humidity   : {main.get('humidity', 'N/A')}%",
        f"Pressure   : {main.get('pressure', 'N/A')} hPa",
        f"Clouds     : {cloud_pct}% coverage",
    ]

    wind = wx.get("wind", {})
    if wind:
        speed = wind.get("speed")
        gust = wind.get("gust")
        direction = wind.get("deg")
        # OpenWeather returns m/s for metric/standard, mph for imperial
        speed_unit = "mph" if units == "imperial" else "m/s"
        wind_parts = []
        if speed is not None:
            wind_parts.append(f"{speed} {speed_unit}")
        if direction is not None:
            wind_parts.append(f"{direction}°")
        if gust is not None:
            wind_parts.append(f"gusts {gust} {speed_unit}")
        if wind_parts:
            lines.append(f"Wind       : {', '.join(wind_parts)}")

    lines.append("----------------------------------------")
    return "\n".join(lines)


def perform_lookup(units):
    """
    Handle one lookup based on the user's menu choice.

    Args:
        units (str): The units to use for the weather data.

    Returns:
        None

    Raises:
        SystemExit: If the user chooses to quit.
    """
    choice = input_menu_choice()
    if choice == 3:
        print("Goodbye! Thanks for using Jacob's Weather Lookup.")
        sys.exit(0)

    if choice == 1:
        zip_code = input_zip_code()
        location = geocode_by_zip(zip_code)
    else:
        city, state = input_city_state()
        location = geocode_by_city_state(city, state)

    if not location:
        print("Could not determine location. Please try again.")
        return

    # Fetch weather using lat/lon
    try:
        lat = float(location["lat"])
        lon = float(location["lon"])
    except (KeyError, ValueError):
        print("Internal error: invalid coordinates from geocoding.")
        return

    weather = fetch_current_weather(lat, lon, units)
    if not weather:
        print("Could not fetch weather for that location. Please try again.")
        return

    # Display nicely
    report = format_weather_report(location, weather, units)
    print(report)


def ask_continue():
    """
    Ask if the user wants to perform another lookup.

    Returns:
        bool: True if the user wants to perform another lookup, False if the user wants to quit.
    """
    while True:
        again = input("\nLook up another location? (y/n): ").strip().lower()
        if again in ("y", "yes"):
            return True
        if again in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def main():
    """
    Entry point. Select units, then allow repeated lookups until the user quits.
    """
    print("Welcome to Jacob's Weather Lookup CLI (U.S. only)")
    units = input_units_choice()

    # Main loop for multiple lookups
    while True:
        perform_lookup(units)
        if not ask_continue():
            print("Thanks for using Jacob's Weather Lookup. Stay comfy out there!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Goodbye!")