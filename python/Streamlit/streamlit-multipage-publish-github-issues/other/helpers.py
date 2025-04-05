import asyncio
from urllib.parse import urlparse

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
    Extracts the GitHub repository owner and name from a given URL.

    Parameters:
    - url (str): The GitHub URL from which to extract the repository owner and name.

    Returns:
    - tuple: A tuple containing the repository owner and name, or (None, None) if not found.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Split the path into segments
    path_segments = parsed_url.path.strip('/').split('/')
    
    # Ensure the URL is a GitHub URL and has at least two path segments (owner and repo name)
    if 'github.com' in parsed_url.netloc and len(path_segments) >= 2:
        return path_segments[0], path_segments[1]
    
    return None, None
