import streamlit as st
from typing import List
import plotly.express as px
import pandas as pd
import json
import asyncio
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

def render_observable_facet_chart(facets: List[QueryContentsFacetsContentsFacets]):
    json_strings = [facet.model_dump_json(indent=2) for facet in facets]  # Using indent for pretty printing
    json_dicts = [json.loads(js) for js in json_strings]

    df = pd.json_normalize(json_dicts, sep='_')
    
    # Rename columns for clarity
    df.rename(columns={
        'observable_type': 'Type',
        'observable_observable_name': 'Name',
        'count': 'Count'
    }, inplace=True)
    
    # Sort the DataFrame by 'Name' alphabetically
    df = df.sort_values(by='Name')
    
    # Using Plotly for more customizable visualization
    fig = px.bar(df, x='Name', y='Count', color='Type', 
                 hover_data={'Name': True, 'Count': True, 'Type': True},
                 labels={'Count': 'Count', 'Name': 'Observable Name', 'Type': 'Observable Type'})
        
    # Render the Plotly figure in Streamlit
    st.plotly_chart(fig)            