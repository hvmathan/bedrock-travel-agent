# AI Travel Agent with AWS Bedrock AgentCore

A sophisticated AI-powered travel booking system built with modular architecture, designed for integration with Amazon Bedrock AgentCore.

## 🎯 Project Overview

This project demonstrates building a complete travel agent system that can search flights, hotels, manage bookings, and plan itineraries. The system is architected to eventually integrate with AWS Bedrock AgentCore for production deployment.

## 📖 Background & Learning Journey

### Phase 1: Foundation & Concepts
For detailed background on AWS Bedrock AgentCore and the initial conceptual framework, please refer to this comprehensive blog post:

**[Building a Proactive AI Travel Agent on AWS: My Journey with Bedrock AgentCore - Part 1](https://dev.to/aws-builders/building-a-proactive-ai-travel-agent-on-aws-my-journey-with-bedrock-agentcore-part-1-36c7)**

This blog covers:
- Understanding AWS Bedrock AgentCore
- Architecture design principles
- Initial planning and concept development
- Foundation setup considerations

## 🚀 Phase 2: Current Implementation

### What We've Built So Far

✅ **Complete Local Travel Agent System**
- Fully functional orchestrator that coordinates all components
- Natural language processing for user intent recognition
- Mock travel APIs with realistic data
- Complete booking workflow with confirmation codes
- Budget calculation and itinerary planning utilities

✅ **Modular Architecture Ready for Bedrock**
- Separation of concerns (planning, execution, orchestration)
- Tool-based architecture compatible with Bedrock AgentCore
- Standardized interfaces for easy integration
- Comprehensive error handling and logging

## 🏗️ System Architecture

```
User Input → Orchestrator → Planning Agent → Travel Tools → Response
```

### Core Components

1. **`orchestrator.py`** - Main controller and entry point
   - Coordinates between all components
   - Handles user requests and routes to appropriate tools
   - Manages the complete request-response lifecycle

2. **`planning_agent.py`** - AI reasoning engine
   - Analyzes user input and extracts intent
   - Determines required actions and parameters
   - Creates structured execution plans

3. **`travel_tool.py`** - Execution layer
   - Implements flight and hotel search functionality
   - Provides both formatted and structured data responses
   - Ready for real API integration

4. **`mock_travel_api.py`** - Comprehensive mock backend
   - Realistic travel data for testing
   - Simulates real travel API responses
   - Supports flights, hotels, and booking operations

5. **`booking_tools.py`** - Complete booking management
   - Booking creation and confirmation
   - Booking history tracking
   - Cancellation and modification support

6. **`planning_tools.py`** - Advanced planning utilities
   - Budget calculations and cost estimations
   - Date parsing and validation
   - Itinerary generation and optimization

## 🛠️ Current Features

### Implemented Functionality
- ✈️ **Flight Search**: Search flights between any two locations
- 🏨 **Hotel Search**: Find accommodations in any city
- 💰 **Budget Planning**: Cost calculations and budget estimation
- 📅 **Itinerary Planning**: Trip planning and scheduling
- 📝 **Booking Management**: Complete booking lifecycle
- 🤖 **Natural Language Processing**: Understands travel-related queries
- 🎯 **Intent Recognition**: Accurately determines user needs

### Sample Interactions
```
User: "Find flights from NYC to London"
Agent: Searches and returns available flights with prices and times

User: "I need hotels in Tokyo for next week"  
Agent: Returns hotel options with ratings, prices, and amenities

User: "Plan a 5-day trip to Paris"
Agent: Provides itinerary suggestions and cost estimates
```

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- VS Code (recommended)
- Git

### Installation & Setup
```bash
# Clone the repository
git clone https://github.com/hvmathan/bedrock-travel-agent.git
cd bedrock-travel-agent

# Install dependencies (if any)
pip install -r requirements.txt  # Create this file as needed

# Run the orchestrator
python orchestrator.py
```

### Testing the System
The orchestrator includes both automated test cases and interactive mode:

1. **Automated Tests**: Run predefined test scenarios
2. **Interactive Mode**: Chat directly with the travel agent
3. **Component Testing**: Test individual components separately

## 📁 Project Structure

```
bedrock-travel-agent/
├── orchestrator.py          # Main controller and entry point
├── planning_agent.py        # AI reasoning and intent analysis
├── travel_tool.py          # Flight and hotel search tools
├── mock_travel_api.py      # Mock backend with realistic data
├── booking_tools.py        # Complete booking management
├── planning_tools.py       # Advanced planning utilities
├── my_agent.py            # Future Bedrock AgentCore integration
├── run_agent.py           # Alternative Bedrock entry point
└── README.md              # This file
```

## 🎯 Next Steps: Bedrock Integration

### Phase 3: AWS Bedrock AgentCore Integration
- [ ] Define tool schemas for Bedrock compatibility
- [ ] Register tools with AgentCore framework
- [ ] Configure agent instructions and capabilities
- [ ] Implement tool execution callbacks
- [ ] Test integration with Bedrock's tool calling system
- [ ] Deploy to AWS infrastructure

### Current Status
✅ **Ready for Bedrock Integration**
- All business logic implemented and tested
- Modular architecture compatible with AgentCore
- Tools ready for registration with Bedrock
- Complete functionality validated locally

## 🔧 Technical Highlights

- **Modular Design**: Easy to extend and modify
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging for debugging and monitoring
- **Mock Data**: Realistic test data for development
- **Scalable Architecture**: Ready for production deployment

## 🤝 Contributing

This project is part of a learning journey with AWS Bedrock AgentCore. Feel free to:
- Suggest improvements
- Report issues
- Share integration experiences
- Contribute to Bedrock integration efforts

## 📚 Resources

- [AWS Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock/)
- [Building AI Agents with Bedrock](https://aws.amazon.com/bedrock/agents/)
- [Part 1 Blog Post](https://dev.to/aws-builders/building-a-proactive-ai-travel-agent-on-aws-my-journey-with-bedrock-agentcore-part-1-36c7)

## 📄 License

This project is for educational and demonstration purposes as part of exploring AWS Bedrock AgentCore capabilities.

---

**Current Phase**: ✅ Local Implementation Complete → 🎯 Ready for Bedrock Integration

*Built with passion for AI and travel technology* 🚀
