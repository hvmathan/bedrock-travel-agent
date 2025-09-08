"""
AWS Bedrock AgentCore Travel Agent
Migration from local orchestrator.py to AgentCore Runtime
"""

import os
import asyncio
import json
from typing import Dict, Any, List
from strands import Agent
from strands.models import BedrockModel
from strands.tools import Tool
import boto3
from botocore.exceptions import ClientError

class TravelAgentCore:
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-west-2')
        
        # Initialize Bedrock models
        self.orchestrator_model = BedrockModel(
            model_id="us.amazon.nova-premier-v1:0",
            region=self.region
        )
        
        self.booking_model = BedrockModel(
            model_id="anthropic.claude-3-5-sonnet-20241022-v2:0", 
            region=self.region
        )
        
        # Initialize AgentCore services
        self.memory_client = self._init_memory()
        self.gateway_client = self._init_gateway()
        
        # Initialize agents
        self.orchestrator_agent = self._create_orchestrator_agent()
        self.booking_agent = self._create_booking_agent()
        self.planning_agent = self._create_planning_agent()

    def _init_memory(self):
        """Initialize AgentCore Memory service"""
        try:
            from bedrock_agentcore import Memory
            return Memory(
                memory_id="travel-agent-memory",
                region=self.region
            )
        except ImportError:
            print("AgentCore Memory not available, using local storage")
            return None

    def _init_gateway(self):
        """Initialize AgentCore Gateway for external APIs"""
        try:
            from bedrock_agentcore import Gateway
            return Gateway(
                gateway_id="travel-gateway",
                region=self.region
            )
        except ImportError:
            print("AgentCore Gateway not available, using direct calls")
            return None

    def _create_orchestrator_agent(self) -> Agent:
        """Create the main orchestrator agent"""
        
        orchestrator_tools = [
            self._create_booking_tool(),
            self._create_planning_tool(),
            self._create_memory_tool(),
        ]
        
        orchestrator_prompt = """
        You are a travel orchestrator agent. Your role is to:
        1. Understand user travel requests
        2. Delegate tasks to specialized agents (booking, planning)
        3. Remember user preferences using memory
        4. Coordinate responses to provide comprehensive travel plans
        
        Available tools:
        - booking_agent: Handle flight, hotel, car rental bookings
        - planning_agent: Create itineraries and recommendations  
        - memory_tool: Store and retrieve user preferences
        
        Always provide helpful, accurate travel assistance.
        """
        
        return Agent(
            model=self.orchestrator_model,
            tools=orchestrator_tools,
            system_prompt=orchestrator_prompt
        )

    def _create_booking_agent(self) -> Agent:
        """Create specialized booking agent"""
        
        booking_tools = [
            self._create_flight_search_tool(),
            self._create_hotel_search_tool(),
            self._create_booking_confirmation_tool()
        ]
        
        booking_prompt = """
        You are a booking specialist agent. You handle:
        1. Flight searches and bookings
        2. Hotel searches and reservations
        3. Car rental bookings
        4. Travel insurance options
        
        Use the available tools to provide accurate pricing and availability.
        Always confirm booking details before finalizing.
        """
        
        return Agent(
            model=self.booking_model,
            tools=booking_tools,
            system_prompt=booking_prompt
        )

    def _create_planning_agent(self) -> Agent:
        """Create planning specialist agent"""
        
        planning_tools = [
            self._create_itinerary_tool(),
            self._create_weather_tool(),
            self._create_attractions_tool()
        ]
        
        planning_prompt = """
        You are a travel planning specialist. You create:
        1. Detailed itineraries
        2. Restaurant recommendations
        3. Activity suggestions
        4. Weather-based advice
        
        Consider user preferences, budget, and travel dates.
        """
        
        return Agent(
            model=self.orchestrator_model,
            tools=planning_tools,
            system_prompt=planning_prompt
        )

    def _create_booking_tool(self) -> Tool:
        """Tool to delegate to booking agent"""
        async def booking_delegate(query: str) -> str:
            try:
                response = await self.booking_agent.run(query)
                return response.content
            except Exception as e:
                return f"Booking error: {str(e)}"
        
        return Tool(
            name="booking_agent",
            description="Delegate booking-related queries to the booking specialist",
            function=booking_delegate
        )

    def _create_planning_tool(self) -> Tool:
        """Tool to delegate to planning agent"""
        async def planning_delegate(query: str) -> str:
            try:
                response = await self.planning_agent.run(query)
                return response.content
            except Exception as e:
                return f"Planning error: {str(e)}"
        
        return Tool(
            name="planning_agent", 
            description="Delegate planning and itinerary queries to the planning specialist",
            function=planning_delegate
        )

    def _create_memory_tool(self) -> Tool:
        """Tool to store/retrieve user preferences"""
        async def memory_operation(operation: str, data: Dict[str, Any] = None) -> str:
            if not self.memory_client:
                return "Memory service not available"
                
            try:
                if operation == "store":
                    await self.memory_client.add_memory(data)
                    return "Preferences stored successfully"
                elif operation == "retrieve":
                    memories = await self.memory_client.get_memories(
                        query=data.get("query", "")
                    )
                    return json.dumps(memories)
                else:
                    return "Invalid memory operation"
            except Exception as e:
                return f"Memory error: {str(e)}"
        
        return Tool(
            name="memory_tool",
            description="Store and retrieve user travel preferences",
            function=memory_operation
        )

    def _create_flight_search_tool(self) -> Tool:
        """Tool for flight searches via Gateway"""
        async def search_flights(origin: str, destination: str, date: str) -> str:
            # Use AgentCore Gateway if available, otherwise direct API
            if self.gateway_client:
                try:
                    response = await self.gateway_client.call(
                        endpoint="travel_api",
                        path="/flights/search",
                        params={
                            "origin": origin,
                            "destination": destination, 
                            "date": date
                        }
                    )
                    return response
                except Exception as e:
                    return f"Flight search error: {str(e)}"
            else:
                # Fallback to mock data
                return f"Mock flight results for {origin} to {destination} on {date}"
        
        return Tool(
            name="search_flights",
            description="Search for flights between origin and destination",
            function=search_flights
        )

    def _create_hotel_search_tool(self) -> Tool:
        """Tool for hotel searches"""
        async def search_hotels(location: str, checkin: str, checkout: str) -> str:
            if self.gateway_client:
                try:
                    response = await self.gateway_client.call(
                        endpoint="travel_api",
                        path="/hotels/search",
                        params={
                            "location": location,
                            "checkin": checkin,
                            "checkout": checkout
                        }
                    )
                    return response
                except Exception as e:
                    return f"Hotel search error: {str(e)}"
            else:
                return f"Mock hotel results for {location} from {checkin} to {checkout}"
        
        return Tool(
            name="search_hotels",
            description="Search for hotels in specified location and dates",
            function=search_hotels
        )

    def _create_booking_confirmation_tool(self) -> Tool:
        """Tool to confirm bookings"""
        async def confirm_booking(booking_details: Dict[str, Any]) -> str:
            # This would integrate with actual booking APIs via Gateway
            return f"Booking confirmed: {json.dumps(booking_details, indent=2)}"
        
        return Tool(
            name="confirm_booking",
            description="Confirm and finalize travel bookings",
            function=confirm_booking
        )

    def _create_itinerary_tool(self) -> Tool:
        """Tool to create travel itineraries"""
        async def create_itinerary(destination: str, days: int, preferences: str) -> str:
            # Enhanced itinerary creation logic
            return f"Created {days}-day itinerary for {destination} based on: {preferences}"
        
        return Tool(
            name="create_itinerary",
            description="Create detailed travel itineraries",
            function=create_itinerary
        )

    def _create_weather_tool(self) -> Tool:
        """Tool to get weather information"""
        async def get_weather(location: str, date: str) -> str:
            if self.gateway_client:
                try:
                    response = await self.gateway_client.call(
                        endpoint="weather_api",
                        path="/weather",
                        params={"q": location, "dt": date}
                    )
                    return response
                except Exception as e:
                    return f"Weather error: {str(e)}"
            else:
                return f"Mock weather for {location} on {date}: Sunny, 75°F"
        
        return Tool(
            name="get_weather",
            description="Get weather information for travel planning",
            function=get_weather
        )

    def _create_attractions_tool(self) -> Tool:
        """Tool to find attractions and activities"""
        async def find_attractions(location: str, category: str = "all") -> str:
            return f"Top attractions in {location} for category: {category}"
        
        return Tool(
            name="find_attractions",
            description="Find tourist attractions and activities",
            function=find_attractions
        )

    async def process_request(self, user_message: str, session_id: str = None) -> str:
        """Main entry point for processing travel requests"""
        try:
            # Set session context for memory
            if session_id and self.memory_client:
                self.memory_client.set_session_id(session_id)
            
            # Process request through orchestrator
            response = await self.orchestrator_agent.run(user_message)
            return response.content
            
        except Exception as e:
            return f"Error processing request: {str(e)}"

# AgentCore entry point
travel_agent = TravelAgentCore()

async def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """AgentCore handler function"""
    try:
        user_message = event.get("message", "")
        session_id = event.get("session_id", "default")
        
        if not user_message:
            return {
                "statusCode": 400,
                "body": {"error": "No message provided"}
            }
        
        response = await travel_agent.process_request(user_message, session_id)
        
        return {
            "statusCode": 200,
            "body": {"response": response}
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
        }

# For local testing
if __name__ == "__main__":
    import asyncio
    
    async def test_local():
        test_message = "I want to plan a 5-day trip to Japan from New York in March. I prefer mid-range hotels and like cultural attractions."
        response = await travel_agent.process_request(test_message)
        print("Travel Agent Response:")
        print(response)
    
    asyncio.run(test_local())