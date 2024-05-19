import streamlit as st
import asyncio
from typing import Optional, List
from graphlit_api import *

def run_async_task(async_func, *args):
    """
    Run an asynchronous function in a new event loop.

    Args:
    async_func (coroutine): The asynchronous function to execute.
    *args: Arguments to pass to the asynchronous function.

    Returns:
    None
    """
    
    loop = None

    try:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(async_func(*args))
    except:
        # Close the existing loop if open
        if loop is not None:
            loop.close()

        # Create a new loop for retry
        loop = asyncio.new_event_loop()

        return loop.run_until_complete(async_func(*args))
    finally:
        if loop is not None:
            loop.close()

def get_sign_in_url(app, scopes, redirect_url):
    return app.get_authorization_request_url(
        scopes,
        redirect_uri=redirect_url
    )

def render_citations(citations: Optional[List[Optional[PromptConversationPromptConversationMessageCitations]]]):
    for citation in citations:
        emoji = select_emoji(citation.content.type, citation.content.file_type)
        index_emoji = index_to_emoji(citation.index)

        if citation.page_number is not None:
            expander_label = f"{index_emoji} {emoji} {citation.content.file_name}: Page {citation.page_number}"
        else:
            expander_label = f"{index_emoji} {emoji} {citation.content.file_name}"
        
        with st.expander(expander_label):            
            st.markdown(citation.text)

def select_emoji(content_type, file_type):
    # Emoji mappings for content types
    content_emoji_map = {
        "FILE": "📄",  # Default for files, overridden by specific file types below
        "PAGE": "🌐",
        "MESSAGE": "💬",
        "TEXT": "📝",
        "POST": "📰",
        "EMAIL": "📧",
        "EVENT": "📅",
        "ISSUE": "🐛",
    }

    # Emoji mappings for file types (used only if content_type is "FILE")
    file_emoji_map = {
        "VIDEO": "🎥",
        "AUDIO": "🎵",
        "IMAGE": "🖼️",
        "DOCUMENT": "📃",
        "EMAIL": "📧",
        "CODE": "💻",
        "DATA": "📊",
    }

    # Select the appropriate emoji
    if content_type == "FILE" and file_type is not None:
        # Return the emoji corresponding to the specific file type
        return file_emoji_map.get(file_type, "📄")
    else:
        # Return the emoji corresponding to the content type
        return content_emoji_map.get(content_type, "📄")

def index_to_emoji(index):
    # Mapping of index to emoji numbers
    emoji_map = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟",
    }
    # Return the emoji, or the index itself if no emoji available
    return emoji_map.get(index, index)
