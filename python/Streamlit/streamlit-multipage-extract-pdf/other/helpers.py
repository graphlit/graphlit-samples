import streamlit as st
import asyncio
from typing import List
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

def display_observations_as_chips(observations: List[GetContentContentObservations]):
    # Group observations by type
    result = {}
    
    # Define a fixed color lookup table for observable types
    colors = {
        "LABEL": "#FFD700",  # Gold
        "PERSON": "#FF6347",  # Tomato
        "ORGANIZATION": "#4682B4",  # SteelBlue
        # Define more types and their colors as needed
    }
    
    for observation in observations:
        observation_type = observation.type.name
        observable_name = observation.observable.name

        if observation_type not in result:
            result[observation_type] = []
        
        result[observation_type].append(observable_name)
    
    # For each observation type, create a row with type label and chips
    for observation_type, observable_names in result.items():
        # Sort the list of observable names for this type
        observable_names.sort()

        # Create a row for each type
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"**{observation_type}**")
        
        with col2:
            # Fetch the color for each observation type from the lookup table
            chip_color = colors.get(observation_type, "#DDDDDD")  # Default color if type not found
            
            # Adjust chip style and layout
            chips = ''.join([
                f"<span style='padding: 8px 12px; background-color: {chip_color}; border-radius: 5px; margin: 5px; display: inline-block; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-family: Arial, sans-serif; color: #FFFFFF;'>{name}</span>"
                for name in sorted(observable_names)  # Sort names before generating chips
            ])

            st.markdown(f"<div style='display: flex; flex-wrap: wrap;'>{chips}</div>", unsafe_allow_html=True)
