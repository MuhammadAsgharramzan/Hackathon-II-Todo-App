"""
AI Todo Agent using OpenAI Agents SDK
"""
import logging
from typing import Dict, Any, List, Optional
import os
from sqlmodel import Session
from dotenv import load_dotenv

# Import Open Agents SDK components
# Based on user reference:
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
)

from tools.task_tools import TaskTools
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env
load_dotenv()

# Disable tracing if requested (optional)
set_tracing_disabled(disabled=True)

class TodoAgent:
    """
    AI Agent for managing Todo tasks using Open Agents SDK
    """

    def __init__(self):
        # Initialize the client
        api_key = config.GEMINI_API_KEY
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment/config")
        
        self.client = AsyncOpenAI(
            api_key=api_key or "dummy_key", # Prevent crash if missing, but will fail calls
            base_url=base_url,
        )
        
        self.model = OpenAIChatCompletionsModel(
            model="gemini-3-flash-preview", # Using Gemini 3 Flash for OpenAI-compatible endpoint
            openai_client=self.client
        )

    async def process_message(self, user_id: str, message: str, session: Session) -> tuple[str, List[Dict[str, Any]]]:
        """
        Process a user message and return AI response and tool calls
        """
        
        # Define tools as inner functions to capture context (user_id, session)
        # We wrap the existing TaskTools methods.
        
        @function_tool
        def add_task(title: str) -> str:
            """
            Add a new task to the user's list.
            Args:
                title: The content or title of the task.
            """
            try:
                result = TaskTools.add_task(user_id=user_id, title=title, session=session)
                if isinstance(result, dict) and "error" in result:
                    return f"Error: {result['error']}"
                return f"Task added with ID {result['task_id']}."
            except Exception as e:
                return f"Error adding task: {str(e)}"

        @function_tool
        def list_tasks(status: str = "all") -> str:
            """
            List tasks.
            Args:
                status: Filter by status: 'all', 'completed', or 'pending'. Default is 'all'.
            """
            try:
                tasks = TaskTools.list_tasks(user_id=user_id, status=status, session=session)
                if not tasks:
                    return f"No {status} tasks found."
                
                # Format as a string for the LLM
                output = []
                for t in tasks:
                    status_icon = "✅" if t['completed'] else "⭕"
                    output.append(f"{t['id']}. {status_icon} {t['title']}")
                return "\n".join(output)
            except Exception as e:
                return f"Error listing tasks: {str(e)}"

        @function_tool
        def complete_task(task_id: int) -> str:
            """
            Mark a task as completed.
            Args:
                task_id: The numeric ID of the task to complete.
            """
            try:
                result = TaskTools.complete_task(user_id=user_id, task_id=task_id, session=session)
                if isinstance(result, dict) and "error" in result:
                    return f"Error: {result['error']}"
                return f"Task {result['id']} '{result['title']}' marked as completed."
            except Exception as e:
                return f"Error completing task: {str(e)}"
        
        @function_tool
        def delete_task(task_id: int) -> str:
            """
            Delete a task.
            Args:
                task_id: The numeric ID of the task to delete.
            """
            try:
                result = TaskTools.delete_task(user_id=user_id, task_id=task_id, session=session)
                if isinstance(result, dict) and "error" in result:
                    return f"Error: {result['error']}"
                return f"Task {result['id']} '{result['title']}' deleted."
            except Exception as e:
                return f"Error deleting task: {str(e)}"

        # Create the agent with these context-bound tools
        agent = Agent(
            name="TodoAssistant",
            instructions=(
                "You are a helpful Todo assistant. "
                "Manage tasks using the provided tools. "
                "Always be specific about task IDs when confirming actions. "
                "When listing tasks, present them clearly."
            ),
            model=self.model,
            tools=[add_task, list_tasks, complete_task, delete_task],
        )

        try:
            # Run the agent asynchronously
            # The SDK Runner handles the loop of reasoning -> tool call -> response
            result = await Runner.run(agent, message)
            
            # The result object contains the final response
            final_response = str(result.final_output)
            
            # We need to extract tool calls for logging/audit if possible
            # Depending on SDK version, result might have a trace or steps.
            # For now, we'll return an empty list or try to inspect result.
            # Assuming result structure has access to steps.
            # If not easily accessible, we skip detailed tool call logging provided by the wrapper,
            # but the tools themselves (via TaskTools) might log.
            tool_calls = [] 
            
            return final_response, tool_calls
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return "I apologize, but I encountered an error processing your request.", []