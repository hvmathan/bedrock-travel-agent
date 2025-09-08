"""
AWS Bedrock AgentCore Wrapper for Your Existing Orchestrator
This wraps your existing orchestrator.py to work with AgentCore Runtime
"""

from bedrock_agentcore import BedrockAgentCoreApp
import json
import sys
import os
from orchestrator import Orchestrator  # Adjust import based on your orchestrator class name

# Add current directory to path to import your existing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Initialize your existing travel system
print("🚀 Initializing your existing travel agent system...")

orchestrator = None
booking_agent = None
planning_agent = None

try:
    orchestrator = Orchestrator()
    print("✅ TravelOrchestrator initialized successfully")
    
except Exception as e:
    print(f"⚠️  Could not import TravelOrchestrator: {e}")
    try:
        # Try importing orchestrator class with different name
        import orchestrator
        # If orchestrator.py has a class, we'll try to find it
        for attr_name in dir(orchestrator):
            attr = getattr(orchestrator, attr_name)
            if hasattr(attr, '__call__') and not attr_name.startswith('_'):
                print(f"Found callable: {attr_name}")
                if 'orchestrat' in attr_name.lower() or 'travel' in attr_name.lower():
                    orchestrator = attr()
                    print(f"✅ Using {attr_name} as orchestrator")
                    break
    except Exception as e2:
        print(f"⚠️  Could not import orchestrator module: {e2}")

try:
    # Try importing your other agents
    from booking_tools import BookingAgent
    booking_agent = BookingAgent()
    print("✅ BookingAgent initialized")
except:
    print("⚠️  BookingAgent not available")

try:
    from planning_agent import PlanningAgent  
    planning_agent = PlanningAgent()
    print("✅ PlanningAgent initialized")
except:
    print("⚠️  PlanningAgent not available")

@app.entrypoint
def invoke(payload):
    """
    AgentCore entry point that calls your existing orchestrator
    """
    try:
        # Extract the message from AgentCore payload
        user_message = payload.get("message", payload.get("prompt", ""))
        session_id = payload.get("session_id", "default")
        
        print(f"📨 Processing request (session: {session_id}): {user_message[:100]}...")
        
        if not user_message:
            return {
                "result": "Hello! I'm your travel planning assistant powered by AWS Bedrock AgentCore. How can I help you plan your next trip?",
                "status": "success"
            }
        
        # Use your existing orchestrator if available
        if orchestrator:
            try:
                # Try different method names your orchestrator might have
                response = None
                
                if hasattr(orchestrator, 'handle_user_request'):
                    print("📞 Calling orchestrator.handle_user_request()")
                    response = orchestrator.handle_user_request(user_message)
                elif hasattr(orchestrator, 'process_request'):
                    print("📞 Calling orchestrator.process_request()")
                    response = orchestrator.process_request(user_message)
                elif hasattr(orchestrator, 'handle_request'):
                    print("📞 Calling orchestrator.handle_request()")
                    response = orchestrator.handle_request(user_message)
                elif hasattr(orchestrator, 'orchestrate'):
                    print("📞 Calling orchestrator.orchestrate()")
                    response = orchestrator.orchestrate(user_message)
                elif hasattr(orchestrator, 'run'):
                    print("📞 Calling orchestrator.run()")
                    response = orchestrator.run(user_message)
                elif callable(orchestrator):
                    print("📞 Calling orchestrator directly")
                    response = orchestrator(user_message)
                else:
                    print("❌ No suitable method found in orchestrator")
                    available_methods = [method for method in dir(orchestrator) if not method.startswith('_')]
                    response = f"Orchestrator available but no suitable method found. Available methods: {available_methods}"
                
                # Ensure response is a string
                if response is None:
                    response = "No response received from orchestrator"
                elif not isinstance(response, str):
                    response = str(response)
                
                print(f"✅ Orchestrator response: {response[:100]}...")
                
                return {
                    "result": response,
                    "session_id": session_id,
                    "status": "success",
                    "agent": "orchestrator",
                    "powered_by": "AWS Bedrock AgentCore"
                }
                
            except Exception as e:
                print(f"❌ Orchestrator error: {e}")
                import traceback
                traceback.print_exc()
                
                return {
                    "result": f"I encountered an issue processing your travel request: {str(e)}. Please try rephrasing your question or try again.",
                    "session_id": session_id,
                    "status": "error",
                    "error": str(e)
                }
        
        else:
            # Fallback response if orchestrator isn't available
            return {
                "result": f"""I understand you're asking about: "{user_message}"

I'm your travel planning assistant running on AWS Bedrock AgentCore, but I'm currently initializing my local orchestrator system. 

Here's what I can help you with once fully loaded:
🔍 Flight and hotel searches
🗓️ Detailed itinerary planning
🌤️ Weather and packing advice
✅ Booking assistance
💡 Local recommendations

Please try your request again in a moment, or rephrase it as a specific travel question.""",
                "session_id": session_id,
                "status": "initializing"
            }
            
    except Exception as e:
        print(f"❌ AgentCore wrapper error: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "result": "I'm experiencing technical difficulties with my travel planning system. Please try again in a moment.",
            "status": "error",
            "error": str(e)
        }

# Health check endpoint  
@app.route("/health")
def health_check():
    """Health check for AgentCore deployment"""
    return {
        "status": "healthy",
        "service": "AWS Bedrock AgentCore Travel Agent",
        "orchestrator_available": orchestrator is not None,
        "agents": {
            "booking": booking_agent is not None,
            "planning": planning_agent is not None
        },
        "orchestrator_methods": list(dir(orchestrator)) if orchestrator else []
    }

# For local testing and debugging
if __name__ == "__main__":
    print("=" * 70)
    print("🚀 AWS Bedrock AgentCore Travel Agent")
    print("=" * 70)
    print("✅ Your existing orchestrator.py wrapped with AgentCore")
    print("🌐 Local server: http://localhost:8080")
    print("📡 Health check: http://localhost:8080/health")
    print("🔧 Debug info:")
    print(f"   - Orchestrator loaded: {orchestrator is not None}")
    print(f"   - Booking agent loaded: {booking_agent is not None}")
    print(f"   - Planning agent loaded: {planning_agent is not None}")
    
    if orchestrator:
        methods = [m for m in dir(orchestrator) if not m.startswith('_')]
        print(f"   - Available orchestrator methods: {methods}")
    
    print("-" * 70)
    print("🧪 Test commands:")
    print("curl -X POST http://localhost:8080/invocations \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"message\": \"Plan a 5-day trip to Tokyo in March\"}'")
    print()
    print("curl http://localhost:8080/health")
    print("=" * 70)
    
    # Run the AgentCore app
    app.run()