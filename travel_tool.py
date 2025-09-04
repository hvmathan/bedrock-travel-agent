# travel_tool.py
import json
from typing import List, Dict, Any

class TravelTool:
    """
    Tool for searching and booking travel options.
    Connects to mock or real travel APIs.
    """
    
    def search_flights(self, origin: str, destination: str, date: str) -> str:
        """
        Search for available flights between two locations.
        
        Args:
            origin (str): Departure city/airport code
            destination (str): Arrival city/airport code
            date (str): Travel date in YYYY-MM-DD format
            
        Returns:
            str: Formatted string with flight information
        """
        # Mock API response
        flights = [
            {
                "flight_id": "F101",
                "airline": "SkyWings",
                "origin": origin,
                "destination": destination,
                "date": date,
                "departure_time": "08:30",
                "arrival_time": "11:45",
                "price": 349.99
            },
            {
                "flight_id": "F102",
                "airline": "GlobalAir",
                "origin": origin,
                "destination": destination,
                "date": date,
                "departure_time": "12:15",
                "arrival_time": "15:20",
                "price": 419.50
            }
        ]
        
        # Format the response
        result = ""
        for flight in flights:
            result += f"{flight['airline']} Flight {flight['flight_id']}: {origin} → {destination}\n"
            result += f"Date: {date}, Departure: {flight['departure_time']}, Arrival: {flight['arrival_time']}\n"
            result += f"Price: ${flight['price']:.2f}\n\n"
            
        return result
    
    def search_hotels(self, location: str, date: str) -> str:
        """
        Search for available hotels in a location.
        
        Args:
            location (str): City or area name
            date (str): Check-in date in YYYY-MM-DD format
            
        Returns:
            str: Formatted string with hotel information
        """
        # Mock API response
        hotels = [
            {
                "hotel_id": "H201",
                "name": "Grand Plaza Hotel",
                "location": location,
                "date": date,
                "price_per_night": 189.99,
                "rating": 4.7,
                "amenities": ["WiFi", "Pool", "Gym"]
            },
            {
                "hotel_id": "H202",
                "name": "City Center Suites",
                "location": location,
                "date": date,
                "price_per_night": 159.50,
                "rating": 4.2,
                "amenities": ["WiFi", "Breakfast", "Parking"]
            }
        ]
        
        # Format the response
        result = ""
        for hotel in hotels:
            result += f"{hotel['name']} (Rating: {hotel['rating']}/5)\n"
            result += f"Location: {location}, Date: {date}\n"
            result += f"Price: ${hotel['price_per_night']:.2f} per night\n"
            result += f"Amenities: {', '.join(hotel['amenities'])}\n\n"
            
        return result

# Function to be used as a tool in the Agent framework
def search_flights(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """
    Mock flight search function.
    Args:
        origin (str): Departure city/airport code.
        destination (str): Arrival city/airport code.
        date (str): Travel date in YYYY-MM-DD format.

    Returns:
        list[dict]: A list of mock flight options.
    """
    # You can later replace this with an actual API call (e.g., Amadeus)
    return [
        {
            "flight_id": "F101",
            "airline": "SkyWings",
            "origin": origin,
            "destination": destination,
            "date": date,
            "departure_time": "08:30",
            "arrival_time": "11:45",
            "price": 349.99
        },
        {
            "flight_id": "F102",
            "airline": "GlobalAir",
            "origin": origin,
            "destination": destination,
            "date": date,
            "departure_time": "12:15",
            "arrival_time": "15:20",
            "price": 419.50
        }
    ]
