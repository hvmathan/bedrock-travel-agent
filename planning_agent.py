# planning_agent.py
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any

class PlanningAgent:
    """
    The PlanningAgent is responsible for determining the steps needed to fulfill a user request.
    It analyzes user input and creates action plans for the orchestrator.
    """
    
    def __init__(self):
        """Initialize the planning agent."""
        self.supported_actions = [
            "search_flights",
            "search_hotels", 
            "calculate_budget",
            "plan_itinerary"
        ]
    
    def create_plan(self, user_input: str) -> Dict[str, Any]:
        """
        Process the user input and create an action plan.
        
        Args:
            user_input (str): The user's request or query
            
        Returns:
            Dict: The action plan with relevant parameters
        """
        user_input_lower = user_input.lower()
        
        # Flight search requests
        if any(keyword in user_input_lower for keyword in ["flights", "fly", "plane", "airport"]):
            plan = self._extract_flight_details(user_input)
            plan["action"] = "search_flights"
            return plan
            
        # Hotel search requests
        elif any(keyword in user_input_lower for keyword in ["hotels", "stay", "accommodation", "room"]):
            plan = self._extract_hotel_details(user_input)
            plan["action"] = "search_hotels"
            return plan
            
        # Budget calculation requests
        elif any(keyword in user_input_lower for keyword in ["budget", "cost", "price", "money", "expensive"]):
            return {
                "action": "calculate_budget",
                "response": "I can help you calculate travel costs. Please provide details about your trip."
            }
            
        # General planning requests
        elif any(keyword in user_input_lower for keyword in ["plan", "trip", "travel", "vacation", "itinerary"]):
            return {
                "action": "plan_itinerary", 
                "response": "I'd be happy to help plan your trip! Could you tell me your destination and travel dates?"
            }
            
        else:
            # Default response if we can't determine intent
            return {
                "action": "respond",
                "response": "I can help you with:\n- Searching for flights\n- Finding hotels\n- Calculating trip budgets\n- Planning itineraries\n\nWhat would you like to do?"
            }
    
    def _extract_flight_details(self, user_input: str) -> Dict[str, Any]:
        """Extract flight search parameters from user input."""
        # Default values
        default_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        plan = {
            "origin": "JFK",  # Better default
            "destination": "LAX", 
            "date": default_date
        }
        
        try:
            text = user_input.lower()
            print(f"🔍 Parsing flight request: '{user_input}'")
            
            # Pattern 1: "flights from ABC to XYZ" or "flights from ABC-XYZ"
            patterns = [
                # "flights from LHR to CDG"
                r'from\s+([A-Za-z]{3})\s+to\s+([A-Za-z]{3})',
                # "flights from LHR-CDG" or "flights LHR-CDG"
                r'(?:from\s+)?([A-Za-z]{3})\s*[-–]\s*([A-Za-z]{3})',
                # "flights JFK LAX"
                r'flights?\s+([A-Za-z]{3})\s+([A-Za-z]{3})',
                # "from New York to Los Angeles"
                r'from\s+([A-Za-z\s]+?)\s+to\s+([A-Za-z\s]+?)(?:\s|$)',
            ]
            
            origin_found = None
            destination_found = None
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    origin_found = match.group(1).strip()
                    destination_found = match.group(2).strip()
                    print(f"✅ Pattern matched: {origin_found} → {destination_found}")
                    break
            
            if origin_found and destination_found:
                # Convert to airport codes if needed
                plan["origin"] = self._normalize_airport_code(origin_found)
                plan["destination"] = self._normalize_airport_code(destination_found)
                
            print(f"🎯 Final plan: {plan['origin']} → {plan['destination']} on {plan['date']}")
            
            # Extract dates if provided
            date_patterns = [
                r'\b(\d{4}-\d{2}-\d{2})\b',  # 2025-09-15
                r'\b(\d{1,2}/\d{1,2}/\d{4})\b',  # 9/15/2025
                r'\b((?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2})\b'
            ]
            
            for date_pattern in date_patterns:
                dates = re.findall(date_pattern, text, re.IGNORECASE)
                if dates:
                    plan["date"] = dates[0]
                    break
                    
        except Exception as e:
            print(f"❌ Error extracting flight details: {e}")
            # Use defaults if extraction fails
            
        return plan
    
    def _normalize_airport_code(self, location: str) -> str:
        """Convert city names to airport codes or clean up codes."""
        location = location.upper().strip()
        
        # If already a 3-letter code, return as-is
        if len(location) == 3 and location.isalpha():
            return location
        
        # City name mappings
        city_mappings = {
            'NEW YORK': 'JFK',
            'NYC': 'JFK',
            'NEWYORK': 'JFK',
            'LONDON': 'LHR',
            'PARIS': 'CDG',
            'TOKYO': 'NRT',
            'LOS ANGELES': 'LAX',
            'LOSANGELES': 'LAX',
            'SAN FRANCISCO': 'SFO',
            'SANFRANCISCO': 'SFO',
            'CHICAGO': 'ORD',
            'MIAMI': 'MIA',
            'BOSTON': 'BOS',
            'SEATTLE': 'SEA',
            'DENVER': 'DEN',
            'ATLANTA': 'ATL',
            'DALLAS': 'DFW',
            'WASHINGTON': 'DCA',
            'HYDERABAD': 'HYD',
            'KUALA LUMPUR': 'MAS'
        }
        
        return city_mappings.get(location, location[:3] if location else 'JFK')
    
    def _extract_hotel_details(self, user_input: str) -> Dict[str, Any]:
        """Extract hotel search parameters from user input."""
        default_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        plan = {
            "location": "Los Angeles",
            "date": default_date
        }
        
        try:
            text = user_input.lower()
            
            # Extract location - look for "in CITY" or "hotels CITY"
            location_patterns = [
                r'in\s+([A-Za-z\s]+?)(?:\s+for|\s+on|\s*$)',
                r'hotels?\s+([A-Za-z\s]+?)(?:\s+for|\s+on|\s*$)'
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text)
                if match:
                    location = match.group(1).strip().title()
                    if location and len(location) > 1:
                        plan["location"] = location
                    break
            
            # Extract dates
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            dates = re.findall(date_pattern, user_input)
            if dates:
                plan["date"] = dates[0]
                
        except Exception as e:
            print(f"Error extracting hotel details: {e}")
            
        return plan


# For testing the agent independently
if __name__ == "__main__":
    agent = PlanningAgent()
    
    print("🎯 Planning Agent Test Mode")
    print("=" * 40)
    
    test_inputs = [
        "Find flights from NYC to LAX",
        "flights from LHR to CDG",
        "flights from LHR-CDG", 
        "flights JFK LAX",
        "I need hotels in Paris", 
        "What's the budget for a 5-day trip?",
        "Plan my vacation to Tokyo"
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: {test_input}")
        plan = agent.create_plan(test_input)
        print(f"Plan: {json.dumps(plan, indent=2)}")
    
    # Interactive mode
    print("\n" + "="*40)
    print("Interactive mode (type 'quit' to exit):")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            plan = agent.create_plan(user_input)
            print(f"Plan: {json.dumps(plan, indent=2)}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break