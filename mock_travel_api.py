# mock_travel_api.py
from typing import Dict, Any, List, Optional
import json
import random
from datetime import datetime, timedelta

class MockTravelAPI:
    """
    A mock travel API that simulates responses from a real travel booking service.
    This would be replaced with actual API calls in a production environment.
    """
    
    def __init__(self):
        # Mock database of flights
        self.flights_db = self._generate_mock_flights()
        # Mock database of hotels
        self.hotels_db = self._generate_mock_hotels()
        
    def _generate_mock_flights(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate a database of mock flights between popular cities"""
        cities = [
            {"code": "NYC", "name": "New York"},
            {"code": "LAX", "name": "Los Angeles"},
            {"code": "CHI", "name": "Chicago"},
            {"code": "MIA", "name": "Miami"},
            {"code": "SFO", "name": "San Francisco"},
            {"code": "DFW", "name": "Dallas"},
            {"code": "SEA", "name": "Seattle"}
        ]
        
        airlines = [
            "SkyWings", "GlobalAir", "PacificBlue", "AmeriJet", 
            "CoastalAir", "MountainExpress", "EagleFlights"
        ]
        
        flights_db = {}
        
        # Generate flights for next 30 days between all city pairs
        for origin in cities:
            for destination in cities:
                if origin["code"] != destination["code"]:
                    route_key = f"{origin['code']}-{destination['code']}"
                    flights_db[route_key] = []
                    
                    # Generate flights for each date
                    for day_offset in range(30):
                        flight_date = (datetime.now() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
                        
                        # Generate 2-5 flights per day on this route
                        for _ in range(random.randint(2, 5)):
                            # Random departure hour between 6 and 20
                            departure_hour = random.randint(6, 20)
                            departure_minute = random.choice([0, 15, 30, 45])
                            departure_time = f"{departure_hour:02d}:{departure_minute:02d}"
                            
                            # Flight duration between 1-5 hours depending on distance
                            duration_hours = random.randint(1, 5)
                            arrival_dt = datetime.strptime(f"{flight_date} {departure_time}", "%Y-%m-%d %H:%M") + timedelta(hours=duration_hours)
                            arrival_time = arrival_dt.strftime("%H:%M")
                            
                            # Generate price - base $200 plus random component
                            price = 200 + random.randint(50, 300)
                            
                            flight = {
                                "flight_id": f"{origin['code']}{destination['code']}-{random.randint(1000, 9999)}",
                                "airline": random.choice(airlines),
                                "origin": origin["code"],
                                "origin_name": origin["name"],
                                "destination": destination["code"],
                                "destination_name": destination["name"],
                                "date": flight_date,
                                "departure_time": departure_time,
                                "arrival_time": arrival_time,
                                "duration": f"{duration_hours}h {random.randint(0, 59)}m",
                                "price": price,
                                "available_seats": random.randint(1, 50)
                            }
                            
                            flights_db[route_key].append(flight)
        
        return flights_db
        
    def _generate_mock_hotels(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate a database of mock hotels in popular cities"""
        cities = [
            "New York", "Los Angeles", "Chicago", "Miami", 
            "San Francisco", "Dallas", "Seattle"
        ]
        
        hotel_names = [
            "Grand Plaza Hotel", "City Center Suites", "Oceanview Resort", 
            "Metropolitan Inn", "Royal Palms Hotel", "Urban Oasis", 
            "Sunset Boulevard Hotel", "Downtown Luxury Suites",
            "Harbor View Hotel", "Parkside Inn"
        ]
        
        amenities_options = [
            ["WiFi", "Pool", "Gym", "Restaurant", "Bar"],
            ["WiFi", "Breakfast", "Parking", "Pet Friendly"],
            ["WiFi", "Room Service", "Spa", "Conference Room"],
            ["WiFi", "Airport Shuttle", "Fitness Center", "Business Center"]
        ]
        
        hotels_db = {}
        
        for city in cities:
            hotels_db[city] = []
            
            # Generate 5-10 hotels per city
            for i in range(random.randint(5, 10)):
                hotel_id = f"{city[:3].upper()}H{i+100}"
                price = random.randint(80, 500)
                rating = round(random.uniform(3.0, 5.0), 1)
                
                hotel = {
                    "hotel_id": hotel_id,
                    "name": f"{random.choice(hotel_names)}",
                    "location": city,
                    "address": f"{random.randint(100, 999)} {random.choice(['Main', 'Broadway', 'Park', 'Ocean', 'Market'])} St",
                    "price_per_night": price,
                    "rating": rating,
                    "amenities": random.choice(amenities_options),
                    "available_rooms": random.randint(1, 20)
                }
                
                hotels_db[city].append(hotel)
        
        return hotels_db
    
    def search_flights(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        """
        Search for flights matching the given criteria
        
        Args:
            origin (str): Origin airport code (e.g., 'NYC')
            destination (str): Destination airport code (e.g., 'LAX')
            date (str): Flight date in YYYY-MM-DD format
            
        Returns:
            List[Dict]: List of matching flights
        """
        route_key = f"{origin}-{destination}"
        
        if route_key not in self.flights_db:
            return []
        
        # Filter flights by date
        matching_flights = [
            flight for flight in self.flights_db[route_key]
            if flight["date"] == date
        ]
        
        # If no exact matches, return flights for the next available date
        if not matching_flights and route_key in self.flights_db:
            # Get all available dates
            available_dates = sorted(list(set(flight["date"] for flight in self.flights_db[route_key])))
            
            # Find next available date
            next_dates = [d for d in available_dates if d >= date]
            if next_dates:
                next_date = next_dates[0]
                matching_flights = [
                    flight for flight in self.flights_db[route_key]
                    if flight["date"] == next_date
                ]
        
        return matching_flights
    
    def search_hotels(self, location: str, check_in: str) -> List[Dict[str, Any]]:
        """
        Search for hotels in a location
        
        Args:
            location (str): City name
            check_in (str): Check-in date in YYYY-MM-DD format
            
        Returns:
            List[Dict]: List of available hotels
        """
        # Normalize city name - take first word and capitalize
        normalized_location = location.split()[0].capitalize()
        
        matching_hotels = []
        
        # Look for exact matches first
        for city, hotels in self.hotels_db.items():
            if normalized_location in city:
                matching_hotels.extend(hotels)
        
        # If no matches, return hotels from a random city
        if not matching_hotels and self.hotels_db:
            random_city = random.choice(list(self.hotels_db.keys()))
            matching_hotels = self.hotels_db[random_city]
        
        return matching_hotels
    
    def book_flight(self, flight_id: str, passenger_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Book a flight
        
        Args:
            flight_id (str): ID of the flight to book
            passenger_info (Dict): Passenger details
            
        Returns:
            Dict: Booking confirmation
        """
        # Find the flight in our database
        for route, flights in self.flights_db.items():
            for flight in flights:
                if flight["flight_id"] == flight_id:
                    # In a real system, we would check availability and update inventory
                    return {
                        "booking_id": f"BK{flight_id}",
                        "status": "confirmed",
                        "flight": flight,
                        "passenger": passenger_info,
                        "booking_date": datetime.now().strftime("%Y-%m-%d"),
                        "confirmation_code": f"CF{flight_id[-4:]}"
                    }
        
        # Flight not found
        return {
            "error": "Flight not found",
            "status": "failed"
        }
    
    def book_hotel(self, hotel_id: str, guest_info: Dict[str, Any], 
                  check_in: str, check_out: str) -> Dict[str, Any]:
        """
        Book a hotel
        
        Args:
            hotel_id (str): ID of the hotel to book
            guest_info (Dict): Guest details
            check_in (str): Check-in date
            check_out (str): Check-out date
            
        Returns:
            Dict: Booking confirmation
        """
        # Find the hotel in our database
        for city, hotels in self.hotels_db.items():
            for hotel in hotels:
                if hotel["hotel_id"] == hotel_id:
                    # In a real system, we would check availability and update inventory
                    return {
                        "booking_id": f"HB{hotel_id}",
                        "status": "confirmed",
                        "hotel": hotel,
                        "guest": guest_info,
                        "check_in": check_in,
                        "check_out": check_out,
                        "booking_date": datetime.now().strftime("%Y-%m-%d"),
                        "confirmation_code": f"HC{hotel_id[-3:]}"
                    }
        
        # Hotel not found
        return {
            "error": "Hotel not found",
            "status": "failed"
        }


# Create a singleton instance for import
mock_api = MockTravelAPI()

# Example usage:
if __name__ == "__main__":
    # Test the mock API
    api = MockTravelAPI()
    
    # Search flights
    flights = api.search_flights("NYC", "LAX", "2025-09-15")
    print(f"Found {len(flights)} flights from NYC to LAX")
    
    # Search hotels
    hotels = api.search_hotels("Los Angeles", "2025-09-15")
    print(f"Found {len(hotels)} hotels in Los Angeles")
