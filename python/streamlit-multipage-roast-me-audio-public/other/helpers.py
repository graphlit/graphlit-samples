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

def get_file_types_images():
    """
    Show the supported file types for images.
    """
    
    markdown_text = """
| File Type        | File Extension      |
|------------------|---------------------|
| JPEG             | .jpg .jpeg .jpe     |
| PNG              | .png                |
| HEIC             | .heif .heic         |
| WebP             | .webp               |
| Windows Bitmap   | .bmp                |
| TIFF             | .tif .tiff          |
"""
    return markdown_text, None
   
def select_file_types(table_to_show):
    # Display the supported file types based on the selected table
    if table_to_show == "Images":
        file_types_table, extra_info  = get_file_types_images()
        file_types = ["jpg","jpeg","jpe","png","heif","heic","webp","bmp","tif","tiff"]

    return file_types, file_types_table, extra_info

def show_file_type_table(markdown_table):
    """ 
    Display the markdown table full width.
    """
    
    st.markdown("""
<style>
/* Target all tables within the Streamlit app and set them to full width */
table {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
    
    # Display the table in Streamlit using Markdown
    st.markdown(markdown_table, unsafe_allow_html=True)
