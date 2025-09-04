# planning_tools.py
from typing import Dict, Any, List, Union
import json
import math
from datetime import datetime, timedelta

class CodeInterpreter:
    """
    A simple code interpreter that can perform calculations and data manipulations.
    This is a basic version that will be used by the PlanningAgent.
    """
    
    def calculate_trip_budget(self, flight_cost: float, hotel_cost_per_night: float, 
                             nights: int, daily_expenses: float) -> Dict[str, Any]:
        """
        Calculate the total budget for a trip.
        
        Args:
            flight_cost (float): Cost of flight(s)
            hotel_cost_per_night (float): Cost of hotel per night
            nights (int): Number of nights staying
            daily_expenses (float): Estimated daily expenses (food, activities, etc.)
            
        Returns:
            Dict: Breakdown of expenses and total
        """
        hotel_total = hotel_cost_per_night * nights
        daily_total = daily_expenses * (nights + 1)  # +1 for departure day
        total_cost = flight_cost + hotel_total + daily_total
        
        return {
            "flight_cost": flight_cost,
            "hotel_total": hotel_total,
            "daily_expenses_total": daily_total,
            "total_cost": total_cost,
            "breakdown": {
                "flights": f"${flight_cost:.2f}",
                "hotel": f"${hotel_total:.2f} (${hotel_cost_per_night:.2f} × {nights} nights)",
                "daily_expenses": f"${daily_total:.2f} (${daily_expenses:.2f} × {nights + 1} days)",
                "total": f"${total_cost:.2f}"
            }
        }
    
    def calculate_travel_dates(self, departure_date: str, trip_length: int) -> Dict[str, str]:
        """
        Calculate travel dates based on departure date and trip length.
        
        Args:
            departure_date (str): Departure date in YYYY-MM-DD format
            trip_length (int): Number of nights for the trip
            
        Returns:
            Dict: Departure and return dates information
        """
        try:
            departure = datetime.strptime(departure_date, "%Y-%m-%d")
            return_date = departure + timedelta(days=trip_length)
            
            return {
                "departure_date": departure.strftime("%Y-%m-%d"),
                "return_date": return_date.strftime("%Y-%m-%d"),
                "trip_length": f"{trip_length} days",
                "formatted": f"{departure.strftime('%B %d, %Y')} to {return_date.strftime('%B %d, %Y')}"
            }
        except ValueError as e:
            return {"error": f"Invalid date format. Please use YYYY-MM-DD format: {str(e)}"}
    
    def compare_flight_options(self, flights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple flight options and find the best value.
        
        Args:
            flights (List[Dict]): List of flight options with price and details
            
        Returns:
            Dict: Analysis of flight options
        """
        if not flights:
            return {"error": "No flight options provided"}
            
        cheapest = min(flights, key=lambda x: x.get("price", float("inf")))
        
        # Calculate average price
        prices = [flight.get("price", 0) for flight in flights]
        avg_price = sum(prices) / len(prices) if prices else 0
        
        return {
            "num_options": len(flights),
            "price_range": f"${min(prices):.2f} - ${max(prices):.2f}",
            "average_price": f"${avg_price:.2f}",
            "cheapest_option": cheapest,
            "recommendation": "Cheapest option is flight " + cheapest.get("flight_id", "Unknown") + 
                             f" at ${cheapest.get('price', 0):.2f}"
        }


# Tool functions for the Agent framework

def calculate_trip_budget(flight_cost: float, hotel_cost_per_night: float, 
                         nights: int, daily_expenses: float) -> Dict[str, Any]:
    """
    Calculate the total budget for a trip.
    
    Args:
        flight_cost (float): Cost of flight(s)
        hotel_cost_per_night (float): Cost of hotel per night
        nights (int): Number of nights staying
        daily_expenses (float): Estimated daily expenses
        
    Returns:
        Dict: Breakdown of expenses and total
    """
    interpreter = CodeInterpreter()
    return interpreter.calculate_trip_budget(flight_cost, hotel_cost_per_night, nights, daily_expenses)

def calculate_travel_dates(departure_date: str, trip_length: int) -> Dict[str, str]:
    """
    Calculate travel dates based on departure date and trip length.
    
    Args:
        departure_date (str): Departure date in YYYY-MM-DD format
        trip_length (int): Number of nights for the trip
        
    Returns:
        Dict: Departure and return dates information
    """
    interpreter = CodeInterpreter()
    return interpreter.calculate_travel_dates(departure_date, trip_length)
