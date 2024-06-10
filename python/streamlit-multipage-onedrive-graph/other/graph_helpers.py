import streamlit.components.v1 as components
import streamlit as st
import random
import os
import json
from other import helpers
from pyvis.network import Network
from typing import Optional
from graphlit_api import *

def select_emoji(entity_type):
    # Emoji mappings for observable types
    observable_emoji_map = {
        "CONTENT": "📄",  # Page facing up emoji for generic content
        "LABEL": "🏷️",   # Label emoji for categories or tags
        "PERSON": "🧑",  # Person emoji for individuals
        "ORGANIZATION": "🏢",  # Office building emoji for organizations
        "PLACE": "🌍",  # Globe showing Europe-Africa for places
        "PRODUCT": "🛍️",  # Shopping bags emoji for products
        "SOFTWARE": "💻",  # Laptop emoji for software
        "REPO": "🗂️",  # Card index dividers emoji for repositories
        "EVENT": "🎉",  # Party popper emoji for events
    }

    # Return the emoji corresponding to the entity type
    return observable_emoji_map.get(entity_type, "📄")  # Default to page facing up emoji if entity type is unknown

def lookup_node_shape(entity_type, content_type, file_type):
    entity_icon_map = {
        "CONTENT": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf15c", "color": "#aec7e8"}},  # file-text
        "LABEL": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf02b", "color": "#ffbb78"}},   # tag (luggage tag-like)
        "PERSON": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf007", "color": "#98df8a"}},  # user
        "ORGANIZATION": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf1ad", "color": "#ff9896"}},  # building
        "PLACE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf3c5", "color": "#c5b0d5"}},  # globe-americas
        "PRODUCT": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf1b2", "color": "#c49c94"}},  # cube
        "SOFTWARE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf085", "color": "#f7b6d2"}},  # cog
        "REPO": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf1c0", "color": "#c7c7c7"}},  # database
        "EVENT": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf073", "color": "#dbdb8d"}},  # calendar
    }

    content_icon_map = {
        "FILE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf15c", "color": "#aec7e8"}},  # file
        "PAGE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf0ac", "color": "#aec7e8"}},  # globe
        "MESSAGE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf075", "color": "#aec7e8"}},  # comment
        "TEXT": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf15c", "color": "#aec7e8"}},  # file-text
        "POST": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf1ea", "color": "#aec7e8"}},  # newspaper
        "EMAIL": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf0e0", "color": "#aec7e8"}},  # envelope
        "EVENT": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf073", "color": "#aec7e8"}},  # calendar
        "ISSUE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf188", "color": "#aec7e8"}},  # bug
    }

    file_icon_map = {
        "VIDEO": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf03d", "color": "#aec7e8"}},  # video-camera
        "AUDIO": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf028", "color": "#aec7e8"}},  # volume-up
        "IMAGE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf03e", "color": "#aec7e8"}},  # picture-o (image)
        "DOCUMENT": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf15b", "color": "#aec7e8"}},  # file-text-o
        "EMAIL": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf0e0", "color": "#aec7e8"}},  # envelope
        "CODE": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf121", "color": "#aec7e8"}},  # code
        "DATA": {"shape": "icon", "icon": {"face": "FontAwesome", "code": "\uf1c0", "color": "#aec7e8"}},  # database
    }

    if file_type is not None:
        return file_icon_map.get(file_type, content_icon_map.get("FILE"))
    elif content_type is not None:
        return content_icon_map.get(content_type, content_icon_map.get("FILE"))
    else:
        return entity_icon_map.get(entity_type, {"shape": "dot"})  # Default to a simple dot shape if the entity type is unknown

def lookup_node_color(entity_type):
    entity_color_map = {
        "CONTENT": "#aec7e8",  # Soft blue
        "LABEL": "#ffbb78",   # Soft orange
        "PERSON": "#98df8a",  # Pale green
        "ORGANIZATION": "#ff9896",  # Soft red
        "PLACE": "#c5b0d5",  # Soft purple
        "PRODUCT": "#c49c94",  # Soft brown
        "SOFTWARE": "#f7b6d2",  # Light pink
        "REPO": "#c7c7c7",  # Light gray
        "EVENT": "#dbdb8d",  # Soft yellow
    }

    return entity_color_map.get(entity_type, "#ffffff")  # Default to white if entity type is unknown

def parse_metadata(metadata):
    if metadata is None:
        return None, None
    
    o = json.loads(metadata)

    return ContentTypes[o["type"]] if "type" in o else None, FileTypes[o["fileType"]] if "fileType" in o else None

def pretty_print_json(dictionary):
    return '\n'.join(f"{key}: {value}" for key, value in dictionary.items() if not key.startswith('@'))

def parse_title(metadata):
    if metadata is None:
        return None
    
    o = json.loads(metadata)

    if o is not None:
        uri = o["uri"] if "uri" in o else None

        title = pretty_print_json(o)

        if uri is not None:
            return f'URI: {uri}' + '\n' + title
        else:
            return title
    else:
        return None

def parse_label(metadata):
    if metadata is None:
        return None
    
    o = json.loads(metadata)

    file_name = o["fileName"] if "fileName" in o else None

    label = None

    document = o["document"] if "document" in o else None
    audio = o["audio"] if "audio" in o else None
    video = o["video"] if "video" in o else None

    if document is not None and "title" in document:
        label = document["title"]
    elif video is not None and "title" in video:
        label = video["title"]
    elif audio is not None and "title" in audio:
        label = audio["title"]

    return label if label is not None else file_name

def format_relation(relation: str):
    if relation == "observed-by":
        return None
    
    return relation.replace("-", " ")

def create_pyvis_conversation_graph(graph: Optional[PromptConversationPromptConversationGraph]):
    g = create_pyvis_network()

    if graph.nodes is not None:
        for node in graph.nodes:
            content_type = None
            file_type = None
            label = None
            title = None

            if node.type == EntityTypes.CONTENT:
                content_type, file_type = parse_metadata(node.metadata)
                label = parse_label(node.metadata)
                title = f'{node.type.name} [{node.id}]\n' + parse_title(node.metadata)
            else:
                title = f'{node.type.name} [{node.id}]\n' + parse_title(node.metadata)

            shape = lookup_node_shape(node.type.name, content_type, file_type)
            
            g.add_node(node.id, label=label if label is not None else node.name, shape=shape["shape"], icon=shape["icon"], color=lookup_node_color(node.type.name), title=title if title is not None else f'{node.type.name} [{node.id}]')

    if graph.edges is not None:
        for edge in graph.edges:
            # ensure start and end vertex exist in graph
            if not edge.from_ in g.node_ids:
                g.add_node(edge.from_)
            if not edge.to in g.node_ids:
                g.add_node(edge.to)

            relation = format_relation(edge.relation)

            width = 3 if edge.relation != "observed-by" else 1

            g.add_edge(edge.from_, edge.to, label=relation, title=relation, width=width, arrowStrikethrough=False, arrows="middle")

    return g

def create_pyvis_contents_graph(graph: Optional[QueryContentsGraphContentsGraph]):
    g = create_pyvis_network()

    if graph.nodes is not None:
        for node in graph.nodes:
            content_type = None
            file_type = None
            label = None
            title = None

            if node.type == EntityTypes.CONTENT:
                content_type, file_type = parse_metadata(node.metadata)
                label = parse_label(node.metadata)
                title = f'{node.type.name} [{node.id}]\n' + parse_title(node.metadata)
            else:
                title = f'{node.type.name} [{node.id}]\n' + parse_title(node.metadata)

            shape = lookup_node_shape(node.type.name, content_type, file_type)

            g.add_node(node.id, label=label if label is not None else node.name, shape=shape["shape"], icon=shape["icon"], color=lookup_node_color(node.type.name), title=title if title is not None else f'{node.type.name} [{node.id}]')

    if graph.edges is not None:
        for edge in graph.edges:
            # ensure start and end vertex exist in graph
            if not edge.from_ in g.node_ids:
                g.add_node(edge.from_)
            if not edge.to in g.node_ids:
                g.add_node(edge.to)

            relation = format_relation(edge.relation)

            width = 3 if edge.relation != "observed-by" else 1

            g.add_edge(edge.from_, edge.to, label=relation, title=relation, width=width, arrowStrikethrough=False, arrows="middle")

    return g

def create_pyvis_network():
    g = Network(
        notebook=False,
        directed=True,
        cdn_resources="in_line",
        height="900px",
        width="100%",
    )

    return g

def display_pyvis_graph(g):
    g.set_options("""
    var options = {
        "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.01,
                "springLength": 100,
                "springConstant": 0.08
            },
            "maxVelocity": 50,
            "solver": "forceAtlas2Based",
            "timestep": 0.35,
            "stabilization": {
                "iterations": 100
            }
        }
        }
    """)

    # render with random file name
    graph_html = g.generate_html(f"graph_{random.randint(0, 1000)}.html")

    # Inject FontAwesome CSS
    font_awesome_link = '<script src="https://kit.fontawesome.com/2c74303849.js" crossorigin="anonymous"></script>'
    graph_html = graph_html.replace('<head>', f'<head>{font_awesome_link}')

    components.html(graph_html, height=900, scrolling=False)
