# run_agent.py

from bedrock_agentcore import BedrockAgentCoreApp
from orchestrator import Orchestrator  # Correct class name

app = BedrockAgentCoreApp()
orchestrator = Orchestrator()  # Initialize the Orchestrator class

@app.entrypoint
def invoke(payload, context=None):
    user_input = payload.get("prompt", "")
    result = orchestrator.handle_user_request(user_input)
    return {"result": result}

if __name__ == "__main__":
    app.run()
