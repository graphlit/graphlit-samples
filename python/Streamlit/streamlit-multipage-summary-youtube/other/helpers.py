import asyncio
from urllib.parse import urlparse, parse_qs

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

def parse_uri(url):
    """
    Extracts the YouTube video ID from a given URL.

    Parameters:
    - url (str): The URL from which to extract the video ID.

    Returns:
    - str: The extracted YouTube video ID, or None if not found.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Validate the netloc to ensure it's a YouTube URL
    if 'youtube.com' in parsed_url.netloc:
        # Parse the query string
        query_string = parse_qs(parsed_url.query)
        
        # Get the video ID from the 'v' parameter
        video_id = query_string.get('v')
        
        if video_id:
            return video_id[0]
    return None            