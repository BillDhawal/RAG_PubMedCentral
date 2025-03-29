from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from typing import List, Dict
from dotenv import load_dotenv
import os
load_dotenv()

LLM_APIKEY = os.getenv("LLM_APIKEY")

def create_chat_client():
    """Create and return a ChatOpenAI client."""
    return ChatOpenAI(
        model="Qwen2.5-Coder-32B-Instruct",
        openai_api_key=LLM_APIKEY,
        openai_api_base="https://llm-api.cyverse.ai/v1"
    )

def format_chat_history(messages: List[Dict[str, str]]) -> List:
    """
    Format the chat history into LangChain message format.
    
    Args:
        messages (List[Dict]): List of message dictionaries
        
    Returns:
        List: Formatted messages for LangChain
    """
    formatted_messages = [
        SystemMessage(content=(
            "You are a helpful AI assistant. Provide informative "
            "and relevant responses based on the conversation context."
        ))
    ]
    
    for message in messages:
        content = message.get("content", "")
        if message.get("role") == "user":
            formatted_messages.append(HumanMessage(content=content))
        elif message.get("role") == "assistant":
            formatted_messages.append(AIMessage(content=content))
    
    return formatted_messages

def get_llm_response(user_input: str, chat_history: List[Dict[str, str]] = None):
    """
    Get streaming response from the LLM model using chat history for context.
    
    Args:
        user_input (str): Current user message
        chat_history (List[Dict]): Previous messages
        
    Yields:
        str: Tokens from the LLM response as they arrive
    """
    try:
        chat = create_chat_client()
        chat.streaming = True
        
        # Initialize messages with system message if no history
        if chat_history is None:
            chat_history = []
            
        # Format the chat history and add current input
        messages = format_chat_history(chat_history)
        messages.append(HumanMessage(content=user_input))
        
        # Get streaming response from LLM
        for chunk in chat.stream(messages):
            if chunk.content is not None:
                yield chunk.content
                
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        yield error_msg