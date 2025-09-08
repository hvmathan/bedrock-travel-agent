# orchestrator.py

from planning_agent import PlanningAgent
from travel_tool import TravelTool

class Orchestrator:
    """
    The Orchestrator coordinates between the PlanningAgent (reasoning)
    and the TravelTool (execution). It decides what needs to be done
    and calls the appropriate tool(s).
    """

    def __init__(self):
        print("🚀 Initializing Travel Agent Orchestrator...")
        try:
            self.planning_agent = PlanningAgent()
            self.travel_tool = TravelTool()
            print("✅ All components initialized successfully!")
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            raise

    def handle_user_request(self, user_input: str) -> str:
        """
        Main orchestration logic:
        1. Ask the planning agent what steps are needed.
        2. If a tool action is required, execute it.
        3. Return a final combined response.
        """
        print(f"📝 Processing request: {user_input}")
        
        try:
            # Step 1: Create plan using planning agent
            plan = self.planning_agent.create_plan(user_input)
            print(f"🎯 Generated plan: {plan}")
            
            # Step 2: Execute the plan based on action type
            if plan["action"] == "search_flights":
                print("✈️ Searching for flights...")
                flights = self.travel_tool.search_flights(
                    origin=plan.get("origin", "NYC"),
                    destination=plan.get("destination", "LAX"),
                    date=plan.get("date", "2025-09-15")
                )
                return f"🎫 Flight Search Results:\n\n{flights}"

            elif plan["action"] == "search_hotels":
                print("🏨 Searching for hotels...")
                hotels = self.travel_tool.search_hotels(
                    location=plan.get("location", "Los Angeles"),
                    date=plan.get("date", "2025-09-15")
                )
                return f"🏨 Hotel Search Results:\n\n{hotels}"

            elif plan["action"] == "calculate_budget":
                return "💰 Budget calculation feature coming soon! For now, I can search flights and hotels to help estimate costs."

            elif plan["action"] == "plan_itinerary":
                return "📅 Itinerary planning feature coming soon! I can help you search for flights and hotels as a starting point."

            else:
                # Return the response from the planning agent
                return plan.get("response", "I'm not sure how to handle that request yet.")
                
        except Exception as e:
            error_msg = f"❌ Error processing request: {str(e)}"
            print(error_msg)
            return error_msg


def main():
    """Main function for testing the orchestrator"""
    print("🤖 AI Travel Agent - Orchestrator Test Mode")
    print("=" * 50)
    
    try:
        orch = Orchestrator()
        
        # Test with sample inputs
        test_cases = [
            "Find flights from NYC to London",
            "I need hotels in Tokyo", 
            "What's my travel budget?",
            "Plan a trip to Paris"
        ]
        
        print("\n🧪 Running test cases:")
        print("-" * 30)
        for test_input in test_cases:
            print(f"\n📨 Test Input: {test_input}")
            response = orch.handle_user_request(test_input)
            print(f"🤖 Response: {response}")
            print("-" * 50)
        
        # Interactive mode
        print("\n💬 Interactive Mode (type 'quit' to exit):")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Goodbye! Thanks for testing the Travel Agent!")
                    break
                    
                if not user_input:
                    continue
                    
                response = orch.handle_user_request(user_input)
                print(f"\n🤖 Agent: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thanks for testing the Travel Agent!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}")


if __name__ == "__main__":
    main()