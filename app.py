"""
AWS Bedrock AgentCore Wrapper for Your Existing Orchestrator
This wraps your existing orchestrator.py to work with AgentCore Runtime
"""

from bedrock_agentcore import BedrockAgentCoreApp
from starlette.middleware.cors import CORSMiddleware
import json
import sys
import os
from orchestrator import Orchestrator

# Add current directory to path to import your existing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Add CORS middleware to allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your existing travel system
print("🚀 Initializing your existing travel agent system...")

orchestrator = None
booking_agent = None
planning_agent = None

try:
    orchestrator = Orchestrator()
    print("✅ Orchestrator initialized successfully")
    
except Exception as e:
    print(f"⚠️  Could not import Orchestrator: {e}")

try:
    # Try importing your other agents
    from booking_tools import BookingAgent
    booking_agent = BookingAgent()
    print("✅ BookingAgent initialized")
except Exception as e:
    print("⚠️  BookingAgent not available")

try:
    from planning_agent import PlanningAgent  
    planning_agent = PlanningAgent()
    print("✅ PlanningAgent initialized")
except Exception as e:
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
        
        print(f"📨 Processing request (session: {session_id}): {user_message}")
        
        if not user_message:
            return {
                "result": "Hello! I'm your travel planning assistant powered by AWS Bedrock AgentCore. How can I help you plan your next trip?",
                "status": "success"
            }
        
        # Use your existing orchestrator if available
        if orchestrator:
            try:
                response = None
                
                if hasattr(orchestrator, 'handle_user_request'):
                    print("📞 Calling orchestrator.handle_user_request()")
                    response = orchestrator.handle_user_request(user_message)
                else:
                    print("❌ handle_user_request method not found")
                    available_methods = [method for method in dir(orchestrator) if not method.startswith('_')]
                    response = f"Method not found. Available methods: {available_methods}"
                
                # Ensure response is a string
                if response is None:
                    response = "No response received from orchestrator"
                elif not isinstance(response, str):
                    response = str(response)
                
                print(f"✅ Orchestrator response received")
                
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
                "result": f"I understand you're asking about: '{user_message}'. I'm currently initializing my travel system. Please try again in a moment.",
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

# For local testing and debugging
if __name__ == "__main__":
    print("=" * 70)
    print("🚀 AWS Bedrock AgentCore Travel Agent")
    print("=" * 70)
    print("✅ Your existing orchestrator.py wrapped with AgentCore")
    print("🌐 Local server: http://localhost:8080")
    print("🌍 CORS enabled for browser requests")
    print("🔧 Debug info:")
    print(f"   - Orchestrator loaded: {orchestrator is not None}")
    print(f"   - Booking agent loaded: {booking_agent is not None}")
    print(f"   - Planning agent loaded: {planning_agent is not None}")
    
    if orchestrator:
        methods = [m for m in dir(orchestrator) if not m.startswith('_')]
        print(f"   - Available orchestrator methods: {methods}")
    
    print("-" * 70)
    print("🧪 Test with curl:")
    print('curl -X POST http://localhost:8080/invocations \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"message": "Find flights from LHR to MAS"}\'')
    print("=" * 70)
    
    # Run the AgentCore app
    app.run()