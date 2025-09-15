# travel_tool.py
import json
from typing import List, Dict, Any
from flight_api import RealFlightAPI

class TravelTool:
    """
    Tool for searching and booking travel options.
    Now connects to real flight APIs via Aviationstack.
    """
    
    def __init__(self):
        try:
            # Initialize the real flight API
            self.flight_api = RealFlightAPI()
            print("✅ RealFlightAPI initialized successfully")
        except Exception as e:
            print(f"⚠️ Failed to initialize RealFlightAPI: {e}")
            self.flight_api = None
    
    def search_flights(self, origin: str, destination: str, date: str) -> str:
        """
        Search for available flights between two locations using real API.
        
        Args:
            origin (str): Departure city/airport code
            destination (str): Arrival city/airport code
            date (str): Travel date in YYYY-MM-DD format
            
        Returns:
            str: Formatted string with flight information from real API
        """
        if self.flight_api:
            try:
                # Use real flight API
                print(f"🔍 Searching real flights: {origin} → {destination}")
                real_flight_data = self.flight_api.search_flights(origin, destination, date)
                return real_flight_data
            except Exception as e:
                print(f"❌ Error with real flight API: {e}")
                # Fallback to mock data if API fails
                return self._mock_flight_search(origin, destination, date)
        else:
            print("⚠️ RealFlightAPI not available, using mock data")
            return self._mock_flight_search(origin, destination, date)
    
    def _mock_flight_search(self, origin: str, destination: str, date: str) -> str:
        """
        Fallback mock flight search when real API fails.
        """
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
        result = "⚠️ Using fallback data (API temporarily unavailable)\n\n"
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
        # Mock API response (can be upgraded to real hotel API later)
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
    
    def get_flight_status(self, flight_number: str) -> str:
        """
        Get real-time flight status using the flight API.
        """
        if self.flight_api:
            try:
                return self.flight_api.get_real_time_flight_status(flight_number)
            except Exception as e:
                return f"Unable to get flight status for {flight_number}: {e}"
        else:
            return f"Flight API not available. Cannot check status for {flight_number}"
    
    def search_airports(self, query: str) -> str:
        """
        Search for airports by name or code.
        """
        if self.flight_api:
            try:
                airports = self.flight_api.search_airports(query)
                if not airports:
                    return f"No airports found for: {query}"
                
                result = f"Airports matching '{query}':\n\n"
                for airport in airports[:5]:  # Limit to 5 results
                    name = airport.get('airport_name', 'Unknown')
                    code = airport.get('iata_code', 'N/A')
                    city = airport.get('city_name', 'Unknown')
                    country = airport.get('country_name', 'Unknown')
                    
                    result += f"{name} ({code})\n"
                    result += f"Location: {city}, {country}\n\n"
                
                return result
            except Exception as e:
                return f"Error searching airports: {e}"
        else:
            return f"Flight API not available. Cannot search airports for: {query}"

# Function to be used as a tool in the Agent framework
def search_flights(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """
    Flight search function that uses real API.
    Args:
        origin (str): Departure city/airport code.
        destination (str): Arrival city/airport code.
        date (str): Travel date in YYYY-MM-DD format.

    Returns:
        list[dict]: Flight options from real API or fallback mock data.
    """
    try:
        # Initialize the travel tool and get real data
        travel_tool = TravelTool()
        flight_results = travel_tool.search_flights(origin, destination, date)
        
        # For compatibility, return as structured data
        return [
            {
                "flight_results": flight_results,
                "source": "real_api" if travel_tool.flight_api else "fallback_mock",
                "origin": origin,
                "destination": destination,
                "date": date
            }
        ]
    except Exception as e:
        print(f"Error in search_flights function: {e}")
        # Fallback to mock data structure
        return [
            {
                "flight_id": "F101",
                "airline": "SkyWings",
                "origin": origin,
                "destination": destination,
                "date": date,
                "departure_time": "08:30",
                "arrival_time": "11:45",
                "price": 349.99,
                "source": "error_fallback"
            },
            {
                "flight_id": "F102",
                "airline": "GlobalAir",
                "origin": origin,
                "destination": destination,
                "date": date,
                "departure_time": "12:15",
                "arrival_time": "15:20",
                "price": 419.50,
                "source": "error_fallback"
            }
        ]

# Test the integration
if __name__ == "__main__":
    print("Testing updated TravelTool with real flight API...")
    
    try:
        tool = TravelTool()
        print("✅ TravelTool initialized successfully")
        
        # Test flight search
        print("\n=== Flight Search Test ===")
        flights = tool.search_flights("LHR", "CDG", "2025-09-22")
        print("Flight search results:")
        print(flights)
        
        # Test hotel search  
        print("\n=== Hotel Search Test ===")
        hotels = tool.search_hotels("Paris", "2025-09-22")
        print("Hotel search results:")
        print(hotels)
        
        # Test airport search
        print("\n=== Airport Search Test ===")
        airports = tool.search_airports("London")
        print("Airport search results:")
        print(airports)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()