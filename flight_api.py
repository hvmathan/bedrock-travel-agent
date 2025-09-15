"""
Real Flight API Integration using Aviationstack
Replace your mock flight data with real API calls
"""

import requests
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

# Load environment variables from .env file
load_dotenv()

class RealFlightAPI:
    def __init__(self):
        # Get API key from environment variable
        self.api_key = os.getenv('AVIATIONSTACK_API_KEY')
        if not self.api_key or self.api_key == 'your-api-key-here':
            print("⚠️ Warning: AVIATIONSTACK_API_KEY not found in environment variables")
        self.base_url = "http://api.aviationstack.com/v1"
        
    def search_flights(self, origin: str, destination: str, date: str = None) -> str:
        """
        Search for real flights between origin and destination
        """
        try:
            # Convert city names to airport codes if needed
            origin_code = self._get_airport_code(origin)
            destination_code = self._get_airport_code(destination)
            
            print(f"🔍 API call: {origin_code} → {destination_code}")
            
            # Use flights endpoint for real data
            url = f"{self.base_url}/flights"
            
            params = {
                'access_key': self.api_key,
                'dep_iata': origin_code,
                'arr_iata': destination_code,
                'limit': 10
            }
            
            # Don't filter by date - get any available flights
            # The free tier has limited date coverage
            
            response = requests.get(url, params=params, timeout=10)
            print(f"📡 API Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✈️ Found {len(data.get('data', []))} flights")
                
                if data.get('data') and len(data['data']) > 0:
                    return self._format_flight_results(data, origin, destination)
                else:
                    print("⚠️ No flight data in API response")
                    return self._fallback_flight_data(origin, destination, date)
            else:
                print(f"❌ API Error: {response.status_code} - {response.text[:200]}")
                return self._fallback_flight_data(origin, destination, date)
                
        except Exception as e:
            print(f"❌ Flight API error: {e}")
            return self._fallback_flight_data(origin, destination, date)
    
    def get_real_time_flight_status(self, flight_number: str) -> str:
        """
        Get real-time status of a specific flight
        """
        try:
            url = f"{self.base_url}/flights"
            params = {
                'access_key': self.api_key,
                'flight_iata': flight_number,
                'limit': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and len(data['data']) > 0:
                    flight = data['data'][0]
                    return self._format_flight_status(flight)
            
            return f"Flight {flight_number} status not found"
            
        except Exception as e:
            return f"Error checking flight status: {e}"
    
    def search_airports(self, query: str) -> List[Dict]:
        """
        Search for airports by name or code
        """
        try:
            url = f"{self.base_url}/airports"
            params = {
                'access_key': self.api_key,
                'search': query,
                'limit': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            
            return []
            
        except Exception as e:
            print(f"Airport search error: {e}")
            return []
    
    def _get_airport_code(self, city_or_code: str) -> str:
        """
        Convert city names to airport codes
        """
        # Common city to airport code mappings
        city_codes = {
            'new york': 'JFK',
            'nyc': 'JFK',
            'tokyo': 'NRT',
            'london': 'LHR',
            'paris': 'CDG',
            'los angeles': 'LAX',
            'chicago': 'ORD',
            'miami': 'MIA',
            'san francisco': 'SFO',
            'boston': 'BOS',
            'washington': 'DCA',
            'seattle': 'SEA',
            'denver': 'DEN',
            'atlanta': 'ATL',
            'dallas': 'DFW',
            'hyderabad': 'HYD',
            'hyd': 'HYD',
            'lhr': 'LHR',
            'mas': 'MAS',
            'kuala lumpur': 'MAS'
        }
        
        city_lower = city_or_code.lower()
        return city_codes.get(city_lower, city_or_code.upper())
    
    def _format_flight_results(self, data: Dict, origin: str, destination: str) -> str:
        """
        Format API response into readable flight results
        """
        if not data.get('data') or len(data['data']) == 0:
            return self._fallback_flight_data(origin, destination)
        
        results = [f"✈️ Real Flight Results: {origin} → {destination}\n"]
        
        for flight in data['data'][:5]:  # Limit to 5 results
            airline = flight.get('airline', {}).get('name', 'Unknown Airline')
            flight_number = flight.get('flight', {}).get('iata', 'N/A')
            
            departure = flight.get('departure', {})
            arrival = flight.get('arrival', {})
            
            dep_time = departure.get('scheduled', 'N/A')
            arr_time = arrival.get('scheduled', 'N/A')
            
            dep_airport = departure.get('airport', 'N/A')
            arr_airport = arrival.get('airport', 'N/A')
            
            status = flight.get('flight_status', 'scheduled')
            flight_date = flight.get('flight_date', 'N/A')
            
            # Format times if available
            if dep_time != 'N/A' and arr_time != 'N/A':
                try:
                    dep_formatted = datetime.fromisoformat(dep_time.replace('Z', '+00:00')).strftime('%H:%M')
                    arr_formatted = datetime.fromisoformat(arr_time.replace('Z', '+00:00')).strftime('%H:%M')
                except:
                    dep_formatted = dep_time
                    arr_formatted = arr_time
            else:
                dep_formatted = dep_time
                arr_formatted = arr_time
            
            results.append(f"""
{airline} {flight_number}
Date: {flight_date}
Departure: {dep_formatted} from {dep_airport}
Arrival: {arr_formatted} at {arr_airport}
Status: {status.title()}
            """)
        
        return '\n'.join(results)
    
    def _format_flight_status(self, flight: Dict) -> str:
        """
        Format individual flight status
        """
        airline = flight.get('airline', {}).get('name', 'Unknown')
        flight_number = flight.get('flight', {}).get('iata', 'N/A')
        status = flight.get('flight_status', 'unknown')
        
        departure = flight.get('departure', {})
        arrival = flight.get('arrival', {})
        
        return f"""
Flight Status: {airline} {flight_number}
Status: {status.title()}
Departure: {departure.get('airport', 'N/A')} at {departure.get('scheduled', 'N/A')}
Arrival: {arrival.get('airport', 'N/A')} at {arrival.get('scheduled', 'N/A')}
        """
    
    def _fallback_flight_data(self, origin: str, destination: str, date: str = None) -> str:
        """
        Fallback data when API fails or has no results
        """
        if not date:
            date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        return f"""
✈️ Flight Options: {origin} → {destination}
Date: {date}

⚠️ Note: Showing sample data (API limit reached or no results)

SkyWings Flight SW101 - $349.99
Departure: 08:30 → Arrival: 14:45
Duration: 6h 15m

GlobalAir Flight GA456 - $419.50  
Departure: 12:15 → Arrival: 18:20
Duration: 6h 5m

AirLink Flight AL789 - $299.99
Departure: 16:30 → Arrival: 22:45
Duration: 6h 15m

💡 Tip: Get real-time data by upgrading to premium API access
        """

# Usage example
if __name__ == "__main__":
    # Test the API
    flight_api = RealFlightAPI()
    
    # Test flight search
    print("=== Testing Flight Search ===")
    results = flight_api.search_flights("LHR", "CDG")
    print(results)
    
    print("\n=== Testing JFK to LAX ===")
    results2 = flight_api.search_flights("JFK", "LAX")
    print(results2)
    
    print("\n=== Testing Airport Search ===")
    airports = flight_api.search_airports("Tokyo")
    print(f"Found {len(airports)} airports for Tokyo")
    
    print("\n=== Testing Flight Status ===")
    status = flight_api.get_real_time_flight_status("AA123")
    print(status)