# planning_agent.py
import json
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
        plan = {
            "origin": "NYC",  # Default values
            "destination": "LAX", 
            "date": "2025-09-15"
        }
        
        # Simple keyword extraction (can be improved with NLP)
        try:
            text = user_input.lower()
            
            # Extract origin and destination
            if "from" in text and "to" in text:
                from_idx = text.find("from") + 4
                to_idx = text.find("to")
                
                if from_idx < to_idx:
                    origin = user_input[from_idx:to_idx].strip()
                    destination = user_input[text.find("to") + 2:].split()[0].strip()
                    
                    if origin and len(origin) > 0:
                        plan["origin"] = origin.upper()[:3] if len(origin) <= 3 else origin
                    if destination and len(destination) > 0:
                        plan["destination"] = destination.upper()[:3] if len(destination) <= 3 else destination
            
            # Extract dates (basic implementation)
            import re
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            dates = re.findall(date_pattern, user_input)
            if dates:
                plan["date"] = dates[0]
                
        except Exception as e:
            print(f"Error extracting flight details: {e}")
            # Use defaults if extraction fails
            
        return plan
    
    def _extract_hotel_details(self, user_input: str) -> Dict[str, Any]:
        """Extract hotel search parameters from user input."""
        plan = {
            "location": "Los Angeles",
            "date": "2025-09-15"
        }
        
        try:
            text = user_input.lower()
            
            # Extract location
            if " in " in text:
                in_idx = text.find(" in ") + 4
                location = user_input[in_idx:].split()[0].strip()
                if location:
                    plan["location"] = location.title()
            
            # Extract dates
            import re
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
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        plan = agent.create_plan(user_input)
        print(f"Plan: {json.dumps(plan, indent=2)}")