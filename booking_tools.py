# booking_tools.py
import uuid
from datetime import datetime
from typing import Dict, Any, List
import json

class BookingManager:
    """Manages all booking operations and stores booking history"""
    
    def __init__(self):
        self.bookings = []
        self.booking_counter = 1000
    
    def generate_booking_id(self, booking_type: str) -> str:
        """Generate unique booking ID"""
        prefix = "FL" if booking_type == "flight" else "HT"
        self.booking_counter += 1
        return f"{prefix}{self.booking_counter}"
    
    def save_booking(self, booking: Dict[str, Any]) -> None:
        """Save booking to history"""
        self.bookings.append(booking)
    
    def get_booking_history(self) -> List[Dict[str, Any]]:
        """Get all bookings"""
        return self.bookings
    
    def get_booking(self, booking_id: str) -> Dict[str, Any]:
        """Get specific booking by ID"""
        for booking in self.bookings:
            if booking.get("booking_id") == booking_id:
                return booking
        return None

# Global booking manager instance
booking_manager = BookingManager()


def book_flight(flight_id: str, passenger_details: Dict[str, Any], payment_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Book a flight with passenger details.
    
    Args:
        flight_id (str): ID of the flight to book
        passenger_details (Dict): Passenger information
        payment_info (Dict): Payment information (optional for demo)
    
    Returns:
        Dict: Booking confirmation details
    """
    # Mock flight data (in real implementation, would fetch from API)
    mock_flights = {
        "F101": {
            "airline": "SkyWings",
            "flight_number": "SW101",
            "origin": "NYC",
            "destination": "LAX",
            "date": "2025-09-15",
            "departure_time": "08:30",
            "arrival_time": "11:45",
            "price": 349.99,
            "aircraft": "Boeing 737"
        },
        "F102": {
            "airline": "GlobalAir",
            "flight_number": "GA102", 
            "origin": "NYC",
            "destination": "LAX",
            "date": "2025-09-15",
            "departure_time": "12:15",
            "arrival_time": "15:20",
            "price": 419.50,
            "aircraft": "Airbus A320"
        }
    }
    
    # Validate flight exists
    if flight_id not in mock_flights:
        return {
            "success": False,
            "error": f"Flight {flight_id} not found",
            "booking_id": None
        }
    
    # Validate passenger details
    required_fields = ["first_name", "last_name", "email", "phone"]
    missing_fields = [field for field in required_fields if field not in passenger_details]
    
    if missing_fields:
        return {
            "success": False,
            "error": f"Missing passenger details: {', '.join(missing_fields)}",
            "booking_id": None
        }
    
    # Generate booking
    flight_data = mock_flights[flight_id]
    booking_id = booking_manager.generate_booking_id("flight")
    
    booking = {
        "booking_id": booking_id,
        "booking_type": "flight",
        "status": "confirmed",
        "booked_at": datetime.now().isoformat(),
        "flight_details": flight_data,
        "passenger": passenger_details,
        "total_price": flight_data["price"],
        "currency": "USD",
        "confirmation_code": f"CONF{booking_id[-4:]}"
    }
    
    # Save booking
    booking_manager.save_booking(booking)
    
    return {
        "success": True,
        "booking_id": booking_id,
        "confirmation_code": booking["confirmation_code"],
        "flight_details": {
            "airline": flight_data["airline"],
            "flight_number": flight_data["flight_number"],
            "route": f"{flight_data['origin']} → {flight_data['destination']}",
            "date": flight_data["date"],
            "departure": flight_data["departure_time"],
            "arrival": flight_data["arrival_time"]
        },
        "passenger_name": f"{passenger_details['first_name']} {passenger_details['last_name']}",
        "total_price": flight_data["price"],
        "status": "Confirmed"
    }


def book_hotel(hotel_id: str, guest_details: Dict[str, Any], check_in: str, check_out: str, rooms: int = 1) -> Dict[str, Any]:
    """
    Book a hotel room with guest details.
    
    Args:
        hotel_id (str): ID of the hotel to book
        guest_details (Dict): Guest information
        check_in (str): Check-in date (YYYY-MM-DD)
        check_out (str): Check-out date (YYYY-MM-DD)
        rooms (int): Number of rooms to book
    
    Returns:
        Dict: Booking confirmation details
    """
    # Mock hotel data
    mock_hotels = {
        "H201": {
            "name": "Grand Plaza Hotel",
            "address": "123 Downtown Ave, Los Angeles, CA",
            "rating": 4.7,
            "price_per_night": 189.99,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant", "Room Service"],
            "room_type": "Deluxe King Room"
        },
        "H202": {
            "name": "City Center Suites",
            "address": "456 Business District, Los Angeles, CA",
            "rating": 4.2,
            "price_per_night": 159.50,
            "amenities": ["WiFi", "Breakfast", "Parking", "Business Center"],
            "room_type": "Executive Suite"
        }
    }
    
    # Validate hotel exists
    if hotel_id not in mock_hotels:
        return {
            "success": False,
            "error": f"Hotel {hotel_id} not found",
            "booking_id": None
        }
    
    # Validate guest details
    required_fields = ["first_name", "last_name", "email", "phone"]
    missing_fields = [field for field in required_fields if field not in guest_details]
    
    if missing_fields:
        return {
            "success": False,
            "error": f"Missing guest details: {', '.join(missing_fields)}",
            "booking_id": None
        }
    
    # Calculate nights and total cost
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        nights = (check_out_date - check_in_date).days
        
        if nights <= 0:
            return {
                "success": False,
                "error": "Check-out date must be after check-in date",
                "booking_id": None
            }
    except ValueError:
        return {
            "success": False,
            "error": "Invalid date format. Use YYYY-MM-DD",
            "booking_id": None
        }
    
    # Generate booking
    hotel_data = mock_hotels[hotel_id]
    booking_id = booking_manager.generate_booking_id("hotel")
    
    total_price = hotel_data["price_per_night"] * nights * rooms
    
    booking = {
        "booking_id": booking_id,
        "booking_type": "hotel",
        "status": "confirmed",
        "booked_at": datetime.now().isoformat(),
        "hotel_details": hotel_data,
        "guest": guest_details,
        "stay_details": {
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "rooms": rooms
        },
        "total_price": total_price,
        "currency": "USD",
        "confirmation_code": f"HOTEL{booking_id[-4:]}"
    }
    
    # Save booking
    booking_manager.save_booking(booking)
    
    return {
        "success": True,
        "booking_id": booking_id,
        "confirmation_code": booking["confirmation_code"],
        "hotel_details": {
            "name": hotel_data["name"],
            "address": hotel_data["address"],
            "room_type": hotel_data["room_type"],
            "rating": hotel_data["rating"]
        },
        "stay_details": {
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "rooms": rooms
        },
        "guest_name": f"{guest_details['first_name']} {guest_details['last_name']}",
        "total_price": total_price,
        "price_per_night": hotel_data["price_per_night"],
        "status": "Confirmed"
    }


def cancel_booking(booking_id: str, reason: str = "Customer request") -> Dict[str, Any]:
    """
    Cancel an existing booking.
    
    Args:
        booking_id (str): ID of the booking to cancel
        reason (str): Reason for cancellation
    
    Returns:
        Dict: Cancellation confirmation
    """
    booking = booking_manager.get_booking(booking_id)
    
    if not booking:
        return {
            "success": False,
            "error": f"Booking {booking_id} not found"
        }
    
    if booking["status"] == "cancelled":
        return {
            "success": False,
            "error": "Booking is already cancelled"
        }
    
    # Update booking status
    booking["status"] = "cancelled"
    booking["cancelled_at"] = datetime.now().isoformat()
    booking["cancellation_reason"] = reason
    
    return {
        "success": True,
        "booking_id": booking_id,
        "status": "Cancelled",
        "cancelled_at": booking["cancelled_at"],
        "reason": reason,
        "refund_info": "Refund will be processed within 3-5 business days"
    }


def get_booking_details(booking_id: str) -> Dict[str, Any]:
    """
    Get details of a specific booking.
    
    Args:
        booking_id (str): ID of the booking
    
    Returns:
        Dict: Booking details
    """
    booking = booking_manager.get_booking(booking_id)
    
    if not booking:
        return {
            "success": False,
            "error": f"Booking {booking_id} not found"
        }
    
    return {
        "success": True,
        "booking": booking
    }


def list_all_bookings() -> Dict[str, Any]:
    """
    List all bookings made.
    
    Returns:
        Dict: List of all bookings
    """
    bookings = booking_manager.get_booking_history()
    
    return {
        "success": True,
        "total_bookings": len(bookings),
        "bookings": bookings
    }


# Test functions
if __name__ == "__main__":
    print("🧪 Testing Booking Tools")
    print("=" * 40)
    
    # Test flight booking
    print("\n✈️ Flight Booking Test:")
    passenger = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@email.com",
        "phone": "+1-555-0123"
    }
    
    flight_booking = book_flight("F101", passenger)
    if flight_booking["success"]:
        print(f"✅ Flight booked successfully!")
        print(f"   Booking ID: {flight_booking['booking_id']}")
        print(f"   Confirmation: {flight_booking['confirmation_code']}")
        print(f"   Flight: {flight_booking['flight_details']['route']}")
        print(f"   Price: ${flight_booking['total_price']}")
    else:
        print(f"❌ Booking failed: {flight_booking['error']}")
    
    # Test hotel booking
    print("\n🏨 Hotel Booking Test:")
    guest = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@email.com", 
        "phone": "+1-555-0456"
    }
    
    hotel_booking = book_hotel("H201", guest, "2025-09-15", "2025-09-18")
    if hotel_booking["success"]:
        print(f"✅ Hotel booked successfully!")
        print(f"   Booking ID: {hotel_booking['booking_id']}")
        print(f"   Hotel: {hotel_booking['hotel_details']['name']}")
        print(f"   Stay: {hotel_booking['stay_details']['nights']} nights")
        print(f"   Total: ${hotel_booking['total_price']}")
    else:
        print(f"❌ Booking failed: {hotel_booking['error']}")
    
    # Test booking history
    print("\n📋 Booking History:")
    history = list_all_bookings()
    print(f"Total bookings: {history['total_bookings']}")