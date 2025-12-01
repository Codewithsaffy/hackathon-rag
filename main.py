from fastapi import FastAPI, HTTPException
from agents import Agent, Runner, set_tracing_disabled
from agents_instructions import main_agent_instruction
from tools import read_document
from typing import Dict, Any
from models import model
import uvicorn

app = FastAPI()

set_tracing_disabled(True)

# Create the agent with RAG tool
agent = Agent(
    name="Book_Support_Agent",
    instructions=main_agent_instruction,
    model=model,
    tools=[read_document]
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Book Support Agent API is running!",
        "status": "success"
    }


@app.post("/query")
async def query(request: Dict[str, Any]):
    """
    Query endpoint to communicate with the AI agent.
    
    Expects a JSON payload with a 'query' field containing the user's question.
    Example: {"query": "How many chapters are in the book?"}
    """
    try:
        user_query = request.get("query")
        
        if not user_query or not isinstance(user_query, str):
            raise HTTPException(
                status_code=400, detail="Query field is required and must be a string"
            )
        
        # Run the agent with the user's query
        result = await Runner.run(agent, user_query)
        
        # Return the agent's response
        return {
            "success": True,
            "answer": result.final_output,
            "query": user_query,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
