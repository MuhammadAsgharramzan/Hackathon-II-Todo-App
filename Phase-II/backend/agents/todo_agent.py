"""
AI Todo Agent with MCP Tool Integration
This agent follows the Model Context Protocol and uses tools to manage tasks
"""
import logging
from typing import Dict, Any, List, Optional
import re
import json
from sqlmodel import Session
from tools.task_tools import TaskTools

# Configure logging for audit trails
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TodoAgent:
    """
    AI Agent for managing Todo tasks using MCP tools
    """

    def __init__(self):
        self.tools_map = {
            "add_task": TaskTools.add_task,
            "list_tasks": TaskTools.list_tasks,
            "update_task": TaskTools.update_task,
            "complete_task": TaskTools.complete_task,
            "delete_task": TaskTools.delete_task
        }

        # Define patterns for recognizing user intents
        self.intent_patterns = {
            "add_task": [
                r"(?:add|create|remember|make|new|put|store|write down|jot down|save)\s+(?:a\s+|an\s+|the\s+)?(?:task|todo|item|thing|note|to-do|todo item)\s+(?:to\s+|about\s+|regarding\s+|that\s+)?(.+)",
                r"(?:add|create|remember|make|write down|jot down)\s+(.+?)(?:\.|$|please|now|for me)",
                r"(?:i need to|i want to|let me|can you)\s+(?:add|create|remember|make|write down|jot down)\s+(?:a\s+|an\s+|the\s+)?(?:task|todo|item|thing|note|to-do)\s+(.+)",
            ],
            "list_tasks": [
                r"(?:show|list|display|view|see|what.*(?:are|is)|fetch|get|retrieve|tell me|give me|enumerate|print out|show me)\s*(?:my\s+)?(?:tasks|todos|items|things|notes|list|to-dos|todo list|current tasks|outstanding tasks|pending tasks|all tasks)",
                r"(?:what|how many|which|do i have)\s*(?:tasks|todos|items|things|notes|list|to-dos|current tasks|outstanding tasks|pending tasks|all tasks)",
                r"(?:show|list|display|view|see|what.*(?:are|is)|fetch|get|retrieve|tell me)\s*(?:my\s+)?(?:completed|done|finished|marked|closed)\s*(?:tasks|todos|items|things|notes|list|to-dos)",
                r"(?:show|list|display|view|see|what.*(?:are|is)|fetch|get|retrieve|tell me)\s*(?:my\s+)?(?:pending|incomplete|open|remaining|unfinished)\s*(?:tasks|todos|items|things|notes|list|to-dos)",
            ],
            "complete_task": [
                r"(?:complete|done|finish|mark.*done|check|tick off|accomplish|close|resolve|finish up)\s+(?:task|item|todo|to-do)\s*(?:#|no\.?|number|id)?\s*(\d+)",
                r"(?:complete|done|finish|mark.*done|check|tick off|accomplish|close|resolve|finish up).*?(?:task|item|todo|to-do).*?(\d+)",
                r"(?:complete|done|finish|mark.*done|check|tick off|accomplish|close|resolve|finish up)\s*(?:task|item|todo|to-do)\s*(\d+)",
                r"(?:mark|set|make)\s*(?:task|item|todo|to-do)\s*(?:#|no\.?|number|id)?\s*(\d+)\s*(?:as\s+)?(?:complete|done|finished|closed)",
                r"(\d+)\s*(?:is\s+)?(?:done|complete|finished|closed|accomplished)",
            ],
            "delete_task": [
                r"(?:delete|remove|erase|cancel|kill|drop|get rid of|eliminate|trash|clear|purge)\s+(?:task|item|todo|to-do)\s*(?:#|no\.?|number|id)?\s*(\d+)",
                r"(?:delete|remove|erase|cancel|kill|drop|get rid of|eliminate|trash|clear|purge).*?(?:task|item|todo|to-do).*?(\d+)",
                r"(?:delete|remove|erase|cancel|kill|drop|get rid of|eliminate|trash|clear|purge)\s*(?:task|item|todo|to-do)\s*(\d+)",
            ],
            "update_task": [
                r"(?:update|change|modify|edit|alter|revise|adjust|improve|fix)\s+(?:task|item|todo|to-do)\s*(?:#|no\.?|number|id)?\s*(\d+)",
                r"(?:update|change|modify|edit|alter|revise|adjust|improve|fix)\s*(?:task|item|todo|to-do)\s*(\d+)",
                r"(?:update|change|modify|edit|alter|revise|adjust|improve|fix)\s+(?:task|item|todo|to-do)\s*(?:#|no\.?|number|id)?\s*(\d+)\s+(?:to|with|by)\s+(.+)",
            ]
        }

    def process_message(self, user_id: str, message: str, session: Session) -> tuple[str, List[Dict[str, Any]]]:
        """
        Process a user message and return AI response and tool calls

        Args:
            user_id: The ID of the authenticated user
            message: The user's message
            session: Database session

        Returns:
            Tuple of (assistant_response, tool_calls)
        """
        tool_calls = []

        # Try to match intent patterns
        intent, extracted_params = self._extract_intent_and_params(message)

        if intent and intent in self.tools_map:
            # Execute the appropriate tool
            result = self._execute_tool(intent, user_id, extracted_params)

            if result is not None:
                tool_call = {
                    "tool_name": intent,
                    "arguments": {"user_id": user_id, **extracted_params},
                    "result": result
                }

                # Log tool execution for audit trail
                logger.info(f"Tool executed: {intent} for user {user_id} with params {extracted_params}")

                tool_calls.append(tool_call)

                # Generate natural language response based on tool result
                response = self._generate_response_for_tool(intent, result, extracted_params)
                return response, tool_calls

        # If no intent matched, try to infer from keywords
        response, additional_tool_calls = self._infer_from_keywords(user_id, message)
        tool_calls.extend(additional_tool_calls)

        if not tool_calls:
            # No recognized intent, return helpful guidance
            response = self._provide_helpful_response(message)

        return response, tool_calls

    def _extract_intent_and_params(self, message: str) -> tuple[Optional[str], Dict[str, Any]]:
        """
        Extract intent and parameters from user message using regex patterns
        """
        message_lower = message.lower().strip()

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message_lower, re.IGNORECASE)
                if match:
                    groups = match.groups()

                    if intent == "add_task":
                        if groups:
                            title = groups[-1].strip() if groups[-1] else message
                            # Clean up the title
                            title = re.sub(r'(?:please|now|add|create|remember|make|for me|to do)', '', title, flags=re.IGNORECASE).strip()
                            if title:
                                return intent, {"title": title}

                    elif intent in ["complete_task", "delete_task"]:
                        if groups and groups[0]:
                            try:
                                task_id = int(groups[0])
                                return intent, {"task_id": task_id}
                            except ValueError:
                                continue

                    elif intent == "update_task":
                        if groups and groups[0]:
                            try:
                                task_id = int(groups[0])
                                # Check if there's an additional parameter for update
                                additional_param = None
                                if len(groups) > 1 and groups[1]:
                                    additional_param = groups[1].strip()
                                return intent, {"task_id": task_id, "title": additional_param if additional_param else None}
                            except ValueError:
                                continue

        return None, {}

    def _execute_tool(self, tool_name: str, user_id: str, params: Dict[str, Any]) -> Any:
        """
        Execute the specified tool with given parameters
        """
        if tool_name not in self.tools_map:
            logger.error(f"Unknown tool requested: {tool_name}")
            return None

        tool_func = self.tools_map[tool_name]

        # Prepare arguments for the tool
        tool_args = {"user_id": user_id, **params}

        try:
            # Execute the tool
            result = tool_func(**tool_args)

            # Log the result for audit trail
            if result and isinstance(result, dict) and "error" in result:
                logger.warning(f"Tool {tool_name} executed with error for user {user_id}: {result['error']}")
            else:
                logger.info(f"Tool {tool_name} executed successfully for user {user_id}")

            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name} for user {user_id}: {str(e)}")
            return None

    def _infer_from_keywords(self, user_id: str, message: str) -> tuple[str, List[Dict[str, Any]]]:
        """
        Infer intent from keywords when regex patterns don't match
        """
        message_lower = message.lower()
        tool_calls = []

        # Simple keyword-based inference
        if any(word in message_lower for word in ["add", "create", "remember", "make", "new"]):
            # Try to extract a potential task title
            import re
            # Remove common starting words
            cleaned_message = re.sub(r'^(?:can you |could you |please |pls |add |create |remember |make |i need to |i want to |let me )+', '', message_lower)
            title = cleaned_message.strip()

            if title and len(title) > 0:
                result = TaskTools.add_task(user_id=user_id, title=title)
                if result:
                    if isinstance(result, dict) and "error" in result:
                        # Handle error case
                        return f"❌ Error: {result['error']}", tool_calls
                    else:
                        tool_calls.append({
                            "tool_name": "add_task",
                            "arguments": {"user_id": user_id, "title": title},
                            "result": result
                        })
                        return f"✅ Task '{result['title']}' has been added successfully with ID {result['task_id']}.", tool_calls

        elif any(word in message_lower for word in ["show", "list", "view", "what", "display", "see", "my"]):
            status = "all"
            if "completed" in message_lower or "done" in message_lower or "finished" in message_lower:
                status = "completed"
            elif "pending" in message_lower or "incomplete" in message_lower or "open" in message_lower or "remaining" in message_lower:
                status = "pending"

            tasks = TaskTools.list_tasks(user_id=user_id, status=status)

            tool_calls.append({
                "tool_name": "list_tasks",
                "arguments": {"user_id": user_id, "status": status},
                "result": tasks
            })

            if tasks:
                task_list = "\n".join([f"- {'✅' if t['completed'] else '○'} {t['title']} (ID: {t['id']})" for t in tasks])
                status_text = f" ({status})" if status != "all" else ""
                return f"Here are your{status_text} tasks:\n{task_list}", tool_calls
            else:
                status_text = f" {status}" if status != "all" else ""
                return f"You don't have any{status_text} tasks at the moment.", tool_calls

        elif any(word in message_lower for word in ["done", "complete", "finish", "check", "mark"]):
            # Look for task ID in the message
            task_id_match = re.search(r'\b(\d+)\b', message)
            if task_id_match:
                try:
                    task_id = int(task_id_match.group(1))
                    result = TaskTools.complete_task(user_id=user_id, task_id=task_id)
                    if result:
                        if isinstance(result, dict) and "error" in result:
                            # Handle error case
                            return f"❌ Error: {result['error']}", tool_calls
                        else:
                            tool_calls.append({
                                "tool_name": "complete_task",
                                "arguments": {"user_id": user_id, "task_id": task_id},
                                "result": result
                            })
                            return f"✅ Task '{result['title']}' has been marked as completed.", tool_calls
                    else:
                        return f"❌ Could not find task with ID {task_id}.", tool_calls
                except ValueError:
                    pass

        elif any(word in message_lower for word in ["delete", "remove", "erase", "trash"]):
            # Look for task ID in the message
            task_id_match = re.search(r'\b(\d+)\b', message)
            if task_id_match:
                try:
                    task_id = int(task_id_match.group(1))
                    result = TaskTools.delete_task(user_id=user_id, task_id=task_id)
                    if result:
                        if isinstance(result, dict) and "error" in result:
                            # Handle error case
                            return f"❌ Error: {result['error']}", tool_calls
                        else:
                            tool_calls.append({
                                "tool_name": "delete_task",
                                "arguments": {"user_id": user_id, "task_id": task_id},
                                "result": result
                            })
                            return f"🗑️ Task '{result['title']}' has been deleted successfully.", tool_calls
                    else:
                        return f"❌ Could not find task with ID {task_id}.", tool_calls
                except ValueError:
                    pass

        return "", []  # No action taken

    def _generate_response_for_tool(self, tool_name: str, result: Any, params: Dict[str, Any]) -> str:
        """
        Generate a natural language response based on tool execution result
        """
        if result is None:
            if tool_name == "complete_task":
                return f"❌ I couldn't find a task with that ID. Please check the task ID and try again."
            elif tool_name == "delete_task":
                return f"❌ I couldn't find a task with that ID. Please check the task ID and try again."
            elif tool_name == "update_task":
                return f"❌ I couldn't find a task with that ID. Please check the task ID and try again."
            else:
                return f"❌ Sorry, I encountered an issue processing your request."

        # Check if result contains an error
        if isinstance(result, dict) and "error" in result:
            return f"❌ Error: {result['error']}"

        if tool_name == "add_task":
            return f"✅ Task '{result['title']}' has been added successfully with ID {result['task_id']}."
        elif tool_name == "list_tasks":
            if not result:
                status = params.get('status', 'all')
                status_text = f" {status}" if status != "all" else ""
                return f"You don't have any{status_text} tasks at the moment."

            task_list = "\n".join([f"- {'✅' if t['completed'] else '○'} {t['title']} (ID: {t['id']})" for t in result])
            status = params.get('status', 'all')
            status_text = f" ({status})" if status != "all" else ""
            return f"📋 Here are your{status_text} tasks:\n{task_list}"
        elif tool_name == "complete_task":
            return f"✅ Task '{result['title']}' has been marked as completed."
        elif tool_name == "delete_task":
            return f"🗑️ Task '{result['title']}' has been deleted successfully."
        elif tool_name == "update_task":
            return f"✏️ Task '{result['title']}' has been updated successfully."
        else:
            return f"✅ Action completed successfully."

    def _provide_helpful_response(self, message: str) -> str:
        """
        Provide a helpful response when no specific intent is recognized
        """
        return (f"I understand you said: '{message}'. "
                f"You can ask me to add, list, complete, update, or delete tasks. "
                f"For example: 'Add a task to buy groceries' or 'Show my tasks' or 'Complete task 1'.")