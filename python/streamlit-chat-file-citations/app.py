import streamlit as st
import requests
import jwt
from datetime import datetime
import json
import time
import base64
import os
from graphlit_client import Graphlit

# Initialize session state variables if not already done
if 'client' not in st.session_state:
    st.session_state['client'] = None
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'workflow_id' not in st.session_state:
    st.session_state['workflow_id'] = None
if 'content_id' not in st.session_state:
    st.session_state['content_id'] = None
if 'content_done' not in st.session_state:
    st.session_state['content_done'] = None    
if 'specification_id' not in st.session_state:
    st.session_state['specification_id'] = None
if 'conversation_id' not in st.session_state:
    st.session_state['conversation_id'] = None
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = ""
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = ""
if 'secret_key' not in st.session_state:
    st.session_state['secret_key'] = ""

def ingest_file(name, mimeType, data):
    # Define the GraphQL mutation
    mutation = """
    mutation IngestEncodedFile($name: String!, $mimeType: String!, $data: String!, $workflow: EntityReferenceInput, $isSynchronous: Boolean) {
        ingestEncodedFile(name: $name, mimeType: $mimeType, data: $data, workflow: $workflow, isSynchronous: $isSynchronous) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "isSynchronous": True, # wait for content to be ingested
        "name": name,
        "mimeType": mimeType,
        "data": data,
        "workflow": {
            "id": st.session_state['workflow_id']
        }
    }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['content_id'] = response['data']['ingestEncodedFile']['id']

    return None

def delete_content():
    # Define the GraphQL mutation
    query = """
    mutation DeleteContent($id: ID!) {
        deleteContent(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['content_id']
    }

    response = st.session_state['client'].request(query=query, variables=variables)

def delete_all_contents():
    # Define the GraphQL mutation
    query = """
    mutation DeleteAllContents() {
        deleteAllContents() {
            id
            state
        }
        }
    """

    # Define the variables for the mutation
    variables = {
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_workflow():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateWorkflow($workflow: WorkflowInput!) {
        createWorkflow(workflow: $workflow) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "workflow": {
            "preparation": {
                "jobs": [
                    {
                    "connector": {
                        "type": "AZURE_DOCUMENT_INTELLIGENCE",
                        "azureDocument": {
                            "model": "LAYOUT"
                        }
                    }
                    }
                ]
            },
            "name": "Azure AI Document Intelligence"
        }
    }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['workflow_id'] = response['data']['createWorkflow']['id']

    return None

def delete_workflow():
    # Define the GraphQL mutation
    query = """
    mutation DeleteWorkflow($id: ID!) {
        deleteWorkflow(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['workflow_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_specification():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateSpecification($specification: SpecificationInput!) {
        createSpecification(specification: $specification) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "specification": {
            "type": "COMPLETION",
            "serviceType": "ANTHROPIC",
            "searchType": "VECTOR",
            "anthropic": {
                "model": "CLAUDE_3_HAIKU",
                "temperature": 0.1,
                "probability": 0.2,
                "completionTokenLimit": 2048
            },
            "strategy": { 
                "embedCitations": True,
            },
            "promptStrategy": { 
                "type": "OPTIMIZE_SEARCH" # rewrite for semantic search
            },
            "retrievalStrategy": {
                "type": "SECTION",
            },
            "rerankingStrategy": {
                "serviceType": "COHERE"
            },
            "name": "Completion"
        }
    }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['specification_id'] = response['data']['createSpecification']['id']

    return None

def delete_specification():
    # Define the GraphQL mutation
    query = """
    mutation DeleteSpecification($id: ID!) {
        deleteSpecification(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['specification_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_conversation():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateConversation($conversation: ConversationInput!) {
    createConversation(conversation: $conversation) {
        id
    }
    }
    """

    variables = {
        "conversation": {
            "specification": {
                "id": st.session_state['specification_id']
            },
            # "filter": {
            #     "contents":[
            #         {
            #             "id": st.session_state['content_id']                        
            #         }
            #     ]
            # },
            "name": "Conversation"
        }
    }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['conversation_id'] = response['data']['createConversation']['id']

    return None

def delete_conversation():
    # Define the GraphQL mutation
    query = """
    mutation DeleteConversation($id: ID!) {
        deleteConversation(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['conversation_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def prompt_conversation(prompt):
    # Define the GraphQL mutation
    mutation = """
    mutation PromptConversation($prompt: String!, $id: ID) {
    promptConversation(prompt: $prompt, id: $id) {
        message {
            message
            citations {
                index
                pageNumber
                text
                content {
                    type
                    fileType
                    fileName
                }
            }
        }
    }
    }
    """

    # Define the variables for the mutation
    variables = {
        "prompt": prompt,
        "id": st.session_state['conversation_id']
    }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return None, None, error_message

    message = response['data']['promptConversation']['message']['message']
    citations = response['data']['promptConversation']['message']['citations']

    return message, citations, None

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

def render_citations(citations):
    for citation in citations:
        emoji = select_emoji(citation['content']['type'], citation['content']['fileType'])
        index_emoji = index_to_emoji(citation['index'] + 1)

        if citation['pageNumber'] is not None:
            expander_label = f"{index_emoji} {emoji} {citation['content']['fileName']}: Page {citation['pageNumber']}"
        else:
            expander_label = f"{index_emoji} {emoji} {citation['content']['fileName']}"
        
        with st.expander(expander_label):            
            st.markdown(citation['text'])

def get_file_types_documents():
    """
    Show the supported file types for documents.
    """
    
    markdown_text = """
| File Type               | File Extension       |
|-------------------------|----------------------|
| PDF                     | .pdf                 |
| HTML                    | .htm .html           |
| MIME Archive            | .mhtml               |
| Word Document           | .docx                |
| Excel Spreadsheet       | .xlsx                |
| PowerPoint Presentation | .pptx                |
| Rich Text Format        | .rtf                 |
| Markdown                | .md                  |
| Text                    | .txt .text           |
| Comma-Separated Values  | .csv                 |
| Tab-Separated Values    | .tsv                 |
| Log File                | .log                 |
"""
    return markdown_text, "PDF files will automatically extract and ingest any embedded images, upon file preparation."
       
def get_file_types_audio():
    """
    Show the supported file types for audio.
    """
    
    markdown_text = """
| File Type             | File Extension        |
|-----------------------|-----------------------|
| WAV                   | .wav                  |
| MPEG-4 Audio          | .m4a .aac .mp4        |
| MPEG Audio            | .mpa .m2a             |
| MP3                   | .mp3                  |
| FLAC                  | .flac                 |
| OGG                   | .ogg .opus            |
| AIFF                  | .aiff .aifc .aif      |
| AC-3                  | .ac3                  |
| Windows Media Audio   | .wma                  |
"""
    return markdown_text, None
    
def get_file_types_video():
    """
    Show the supported file types for video.
    """
    
    markdown_text = """
| File Type        | File Extension   |
|------------------|------------------|
| MPEG-4           | .mp4             |
| QuickTime Video  | .mov .moov .qt   |
"""
    return markdown_text, None        

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
   
def get_file_types_animations():
    """
    Show the supported file types for animations.
    """
    
    markdown_text = """
| File Type     | File Extension |
|---------------|----------------|
| GIF           | .gif           |
| Animated PNG  | .apng          |
""" 
    return markdown_text, None
    
def get_file_types_data():
    """
    Show the supported file types for data.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| JSON      | .json          |
| XML       | .xml           |
"""
    return markdown_text, None
     
def get_file_types_emails():
    """
    Show the supported file types for emails.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| EML       | .eml           |
| MSG       | .msg           |
"""
    return markdown_text, "Emails will automatically extract and ingest any attached files, upon file preparation."  
    
def get_file_types_code():
    """
    Show the supported file types for code.
    """
    
    markdown_text = """
| File Type   | File Extension |
|-------------|----------------|
| Python      | .py            |
| JavaScript  | .js            |
| TypeScript  | .ts            |
| Go          | .go            |
| C#          | .cs            |
| C           | .c             |
| C++         | .cpp           |
| Java        | .java          |
| PHP         | .php           |
| Ruby        | .rb            |
| Swift       | .swift         |
| Rust        | .rs            |
"""
    return markdown_text, "Graphlit recognized 50+ code file extensions.  If you find a code file extension we don't support, please reach out to us and we will add it."
    
def get_file_types_packages():
    """
    Show the supported file types for packages.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| ZIP       | .zip           |
"""
    return markdown_text,"Packages will automatically extract and ingest any packaged files, upon file preparation."
    
def get_file_types_other():
    """
    Show the supported file types for other files.
    """
    
    markdown_text = """
| File Type                   | File Extension        |
|-----------------------------|-----------------------|
| Design Web Format           | .dwf .dwfx            |
| AutoCAD DXF                 | .dxf                  |
| Autodesk Drawing            | .dwg                  |
| SVG                         | .svg                  |
| GeoJSON                     | .geojson              |
| ESRI Shapefile              | .shp                  |
| Autodesk FBX                | .fbx                  |
| 3D Studio                   | .3ds                  |
| Collada                     | .dae                  |
| GL Transmission Format      | .gltf .glb            |
| Google Draco                | .drc                  |
| Wavefront                   | .obj                  |
| 3D Systems CAD              | .stl                  |
| Universal Scene Description | .usdz                 |
| LAS                         | .las .laz             |
| E57                         | .e57                  |
| PTS                         | .ptx .pts             |
| PLY                         | .ply                  |
"""
    return markdown_text, None

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

st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Chat with any uploaded file, with citations.  Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).  Chat completion uses the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")

# Radio button to show tables of file types supported
table_to_show = st.radio("Supported file types", ["Documents","Audio","Video","Images","Animations","Data","Emails","Code","Packages","Other"], label_visibility="collapsed", horizontal=True)

# Display the supported file types based on the selected table
file_types = []
extra_info = None
if table_to_show == "Documents":
    file_types_table, extra_info = get_file_types_documents()
    file_types = ["pdf","htm","html","mhtml","docx","xlsx","pptx","rtf","md","txt","text","csv","tsv","log"]
elif table_to_show == "Audio":
    file_types_table, extra_info  = get_file_types_audio()
    file_types = ["wav","m4a","aac","mp4","mpa","m2a","mp3","flac","ogg","opus","aiff","aifc","aif","ac3","wma"]
elif table_to_show == "Video":
    file_types_table, extra_info  = get_file_types_video()
    file_types = ["mp4","mov","moov","qt"]            
elif table_to_show == "Images":
    file_types_table, extra_info  = get_file_types_audio()
    file_types = ["jpg","jpeg","jpe","png","heif","heic","webp","bmp","tif","tiff"]
elif table_to_show == "Animations":
    file_types_table, extra_info  = get_file_types_animations()      
    file_types = ["gif","apng"]      
elif table_to_show == "Data":
    file_types_table, extra_info  = get_file_types_data()
    file_types = ["json","xml"]
elif table_to_show == "Emails":
    file_types_table, extra_info  = get_file_types_emails()
    file_types = ["eml","msg"]
elif table_to_show == "Code":
    file_types_table, extra_info  = get_file_types_code()
    file_types = ["py","js","ts","go","cs","c","cpp","java","php","rb","swift","rs"]
elif table_to_show == "Packages":
    file_types_table, extra_info  = get_file_types_packages()
    file_types = ["zip"]
elif table_to_show == "Other":
    file_types_table, extra_info  = get_file_types_other()
    file_types = ["dwf","dwfx","dxf","dwg","svg","geojson","shp","fbx","3ds","dae","gltf","glb","drc","obj","stl","usdz","las","laz","e57","ptx","pts","ply"]

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")

with st.form("data_content_form"):    
    if file_types:
        # Display the file uploader
        uploaded_file = st.file_uploader("Upload a file", type=file_types, accept_multiple_files=False, label_visibility="collapsed")

        # Display the supported file types table
        show_file_type_table(file_types_table)
        
        if extra_info:
            st.write("")
            st.info(extra_info)

        submit_content = st.form_submit_button("Upload")

        # Now, handle actions based on submit_data outside the form's scope
        if submit_content and uploaded_file:
            st.session_state.messages = []
            st.session_state['content_done'] = False

            if st.session_state['token']:            
                # Clean up previous session state
                if st.session_state['workflow_id'] is None:
                    error_message = create_workflow()

                    if error_message is not None:
                        st.error(f"Failed to create workflow. {error_message}")

                if st.session_state['content_id'] is not None:
                    with st.spinner('Deleting existing content... Please wait.'):
                        delete_content()
                    st.session_state["content_id"] = None

                start_time = time.time()
                    
                # Read the file content
                file_content = uploaded_file.getvalue()
                
                base64_content = base64.b64encode(file_content).decode('utf-8')

                file_name = uploaded_file.name

                # Split the file name into the name and extension
                content_name, _ = os.path.splitext(file_name)

                # Display spinner while processing
                with st.spinner('Ingesting file... Please wait.'):
                    error_message = ingest_file(content_name, uploaded_file.type, base64_content)

                    if error_message is not None:
                        st.error(f"Failed to ingest file. {error_message}")
                    else:
                        duration = time.time() - start_time

                        current_time = datetime.now()
                        formatted_time = current_time.strftime("%H:%M:%S")

                        st.success(f"File ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

                # Once done, notify the user
                st.session_state["content_done"] = True
            else:
                st.error("Please fill in all the connection information.")

with st.form("clear_data_form"):
    st.markdown("If you run into any problems, or exceeded your Free Tier project quota, you can delete all your contents to start over.  Be aware, this deletes *all* the contents in your project.")

    submit_reset = st.form_submit_button("Reset project")

    if submit_reset:
        if st.session_state['token']:
            with st.spinner('Deleting contents... Please wait.'):
                delete_all_contents()

if st.session_state['content_done'] == True:
    if st.session_state['token']:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # render previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if st.session_state['specification_id'] is None:
            error_message = create_specification()

            if error_message is not None:
                st.error(f"Failed to create specification. {error_message}")

        if st.session_state['conversation_id'] is None:
            error_message = create_conversation()

            if error_message is not None:
                st.error(f"Failed to create conversation. {error_message}")

        try:
            if prompt := st.chat_input("Ask me anything about your file."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # render user prompt
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # prompt conversation
                with st.chat_message("assistant"):
                    message, citations, error_message = prompt_conversation(prompt)
                    
                    if error_message is not None:
                        st.error(f"Failed to prompt conversation. {error_message}")
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": message})

                        # render assistant message
                        st.markdown(message)
                        
                        # render citations
                        if citations is not None:
                            render_citations(citations)
        except:
            st.warning("You need to generate a token before chatting with your file.")

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Browse for a file to upload and ingest.
        - **Step 3:** Enter a prompt to ask about the file using [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.
        """)

    with st.form("credentials_form"):
        st.markdown("## 💡 Start here:")
        st.info("Locate connection information for your project in the [Graphlit Developer Portal](https://portal.graphlit.dev/)")

        st.text_input("Organization ID", value=st.session_state['organization_id'], key="organization_id")
        st.text_input("Preview Environment ID", value=st.session_state['environment_id'], key="environment_id")
        st.text_input("Secret", value=st.session_state['secret_key'], key="secret_key")

        submit_credentials = st.form_submit_button("Generate Token")
        
        if submit_credentials:
            if st.session_state['secret_key'] and st.session_state['environment_id'] and st.session_state['organization_id']:
                st.session_state['client'] = Graphlit(environment_id=st.session_state['environment_id'], organization_id=st.session_state['organization_id'], secret_key=st.session_state['secret_key'])
                st.session_state['token'] = st.session_state['client'].token

                st.success("Token generated successfully.")
            else:
                st.error("Please fill in all the connection information.")

    st.markdown("""
        [Support on Discord](https://discord.gg/ygFmfjy3Qx)            
        [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
        [More information](https://www.graphlit.com)      
        """)