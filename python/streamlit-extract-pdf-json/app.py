import streamlit as st
import requests
import jwt
from datetime import datetime
import json
import time
from graphlit_client import Graphlit

# Initialize session state variables if not already done
if 'client' not in st.session_state:
    st.session_state['client'] = None
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'specification_id' not in st.session_state:
    st.session_state['specification_id'] = None
if 'content_id' not in st.session_state:
    st.session_state['content_id'] = None
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = ""
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = ""
if 'secret_key' not in st.session_state:
    st.session_state['secret_key'] = ""
if 'content_done' not in st.session_state:
    st.session_state['content_done'] = None
if 'document_markdown' not in st.session_state:
    st.session_state['document_markdown'] = None
if 'document_metadata' not in st.session_state:
    st.session_state['document_metadata'] = None

def extract_content():
    # Define the GraphQL mutation
    query = """
    mutation ExtractContents($prompt: String!, $specification: EntityReferenceInput!, $filter: ContentFilter) {
        extractContents(prompt: $prompt, specification: $specification, filter: $filter) {
            value
            pageNumber
            error
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "prompt": "Extract data from text into JSON, using the tool provided. If no appropriate data is found, don't return any response.",
        "specification": {
            "id": st.session_state["specification_id"]
        },
        "filter": {
            "id": st.session_state["content_id"]
        }
    }
    response = st.session_state['client'].request(query=query, variables=variables)

#    st.json(response)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return None, error_message

    if 'extractContents' in response['data'] and len(response['data']['extractContents']) > 0:
        deserialized_values = []  # Initialize the list here

        # Attach pageNumber to each deserialized dictionary and add to the list
        for item in response['data']['extractContents']:
            deserialized = json.loads(item['value'])
            deserialized['pageNumber'] = item['pageNumber']
            deserialized_values.append(deserialized)

        # Sort by 'pageNumber'
        sorted_deserialized_values = sorted(deserialized_values, key=lambda x: x['pageNumber'])

        # If you need to remove 'pageNumber' from the final output:
        for item in sorted_deserialized_values:
            item.pop('pageNumber', None)
    
        return sorted_deserialized_values, None
    
    return None, None

def get_content():
    # Define the GraphQL mutation
    query = """
    query GetContent($id: ID!) {
        content(id: $id) {
            id
            state
            markdown
            document {
                title
                keywords
                author
            }          
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['content_id']
    }

    response = st.session_state['client'].request(query=query, variables=variables)

    if 'content' in response['data']:
        return response['data']['content']['document'], response['data']['content']['markdown']
    
    return None

def is_content_done():
    # Define the GraphQL mutation
    query = """
    query IsContentDone($id: ID!) {
        isContentDone(id: $id) {
            result
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state["content_id"]
    }
    response = st.session_state['client'].request(query=query, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return None, error_message

    return response['data']['isContentDone']['result'], None

def delete_specification():
    # Define the GraphQL mutation
    query = """
    mutation DeleteSpecification($id: ID!) {
        deleteSpecification(id: $id) {
            id
            state
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['specification_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_specification(schema):
    # Define the GraphQL mutation
    mutation = """
    mutation CreateSpecification($specification: SpecificationInput!) {
        createSpecification(specification: $specification) {
            id
            name
            state
            type
            serviceType
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "specification": {
            "type": "EXTRACTION",
            "serviceType": "OPEN_AI",
            "openAI": {
                "model": "GPT4_TURBO_128K",
                "temperature": 0.1,
                "probability": 0.2,
                "completionTokenLimit": 2048
            },
            "tools": [
                {
                    "name": "extractJSON",
                    "schema": schema
                }
            ],
            "name": "Extraction"
        }
    }

    # Define the variables for the mutation
    # variables = {
    #     "specification": {
    #         "type": "EXTRACTION",
    #         "serviceType": "MISTRAL",
    #         "mistral": {
    #             "model": "MIXTRAL_8X7B_INSTRUCT",
    #             "temperature": 0.1,
    #             "probability": 0.2,
    #             "completionTokenLimit": 2048
    #         },
    #         "tools": [
    #             {
    #                 "name": "extractJSON",
    #                 "schema": schema
    #             }
    #         ],
    #         "name": "Extraction"
    #     }
    # }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['specification_id'] = response['data']['createSpecification']['id']

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

def ingest_file(uri):
    # Define the GraphQL mutation
    mutation = """
    mutation IngestFile($uri: URL!) {
        ingestFile(uri: $uri) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "uri": uri
    }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['content_id'] = response['data']['ingestFile']['id']

    return None

st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Extract JSON from any PDF, DOCX, or PPTX file. Tool calling done with [Mixtral 8x7B](https://mistral.ai/technology/#models) LLM.")

if st.session_state['token'] is None:
    st.info("To get started, generate a token to connect to your Graphlit project.")

# A dictionary mapping PDF names to their PDF URIs
pdfs = {
#    "Uber Prepared Remarks (Q4 2023)": "https://graphlitplatform.blob.core.windows.net/samples/Uber-Q4-23-Prepared-Remarks.pdf",
    "Microsoft 10Q (March 2024)": "https://graphlitplatform.blob.core.windows.net/samples/MSFT_FY24Q1_10Q.docx",
    "Uber 10Q (March 2022)": "https://graphlitplatform.blob.core.windows.net/samples/uber_10q_march_2022.pdf",
}

document_metadata = None
document_markdown = None

if st.session_state['content_done'] is None:
    st.session_state['content_done'] = False

with st.form("data_content_form"):
    selected_pdf = st.selectbox("Select a PDF:", options=list(pdfs.keys()))
    
    document_uri = st.text_input("Or enter your own URL to a file (i.e. PDF, DOCX, PPTX):", key='pdf_uri')

    uri = document_uri if document_uri else pdfs[selected_pdf]

    submit_content = st.form_submit_button("Submit")

    # Now, handle actions based on submit_data outside the form's scope
    if submit_content and uri:
        st.session_state.messages = []
        st.session_state['content_done'] = False

        if st.session_state['token']:
            st.session_state['uri'] = uri
            
            # Clean up previous session state
            if st.session_state['content_id'] is not None:
                with st.spinner('Deleting existing content... Please wait.'):
                    delete_content()
                st.session_state["content_id"] = None

            error_message = ingest_file(uri)

            if error_message is not None:
                st.error(f"Failed to ingest file [{uri}]. {error_message}")
            else:
                start_time = time.time()

            # Display spinner while processing
            with st.spinner('Ingesting document... Please wait.'):
                done = False
                time.sleep(2)
                while not done:
                    done, error_message = is_content_done()

                    if error_message is not None:
                        st.error(f"Failed to wait for content to be done. {error_message}")
                        done = True                                

                    # Wait a bit before checking again
                    if not done:
                        time.sleep(2)
            # Once done, notify the user
            st.session_state["content_done"] = True

            duration = time.time() - start_time

            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")

            st.success(f"Document ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

            document_metadata, document_markdown = get_content()

            st.session_state['document_metadata'] = document_metadata
            st.session_state['document_markdown'] = document_markdown

            placeholder = st.empty()
        else:
            st.error("Please fill in all the connection information.")

if st.session_state['content_done'] == True:
    if st.session_state['token']:
        if st.session_state['uri'] is not None:
            st.markdown(f"**Document URI:** {st.session_state['uri']}")

        document_metadata = st.session_state['document_metadata']
        document_markdown = st.session_state['document_markdown']

        if document_metadata is not None:
            document_title = document_metadata["title"]
            document_author = document_metadata["author"]

            if document_title is not None:
                st.markdown(f"**Title:** {document_title}")

            if document_author is not None:
                st.markdown(f"**Author:** {document_author}")

        if document_markdown is not None:
            with st.expander("See document text:", expanded=False):
                st.markdown(document_markdown)

        default_schema = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "10Q Financial Document Data Extraction",
  "description": "Schema for extracting key information from 10-Q filings and other financial documents, including company details, financial statements, management's discussion and analysis, controls and procedures, and risk factors.",
  "type": "object",
  "properties": {
    "documentInfo": {
      "type": "object",
      "description": "Basic information about the financial document.",
      "properties": {
        "companyName": {
          "type": "string",
          "description": "The full legal name of the company as reported in the document."
        },
        "cik": {
          "type": "string",
          "description": "Central Index Key (CIK) is a unique identifier assigned by the SEC to all entities who file disclosures."
        },
        "filingDate": {
          "type": "string",
          "format": "date",
          "description": "The date when the document was officially filed with the SEC."
        },
        "fiscalYearEnd": {
          "type": "string",
          "description": "The end date of the fiscal year for which the document reports financial information."
        },
        "formType": {
          "type": "string",
          "description": "The type of SEC form, e.g., 10-Q, 10-K."
        }
      },
      "required": ["companyName", "cik", "filingDate", "formType"]
    },
    "financialStatements": {
      "type": "object",
      "description": "The financial statements section including balance sheets, income statements, and cash flow statements.",
      "properties": {
        "balanceSheets": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/financialStatement"
          },
          "description": "An array of balance sheet statements, capturing the company's financial position at a specific point in time."
        },
        "incomeStatements": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/financialStatement"
          },
          "description": "An array of income statements, detailing the company's revenues, expenses, and profit over a specific period."
        },
        "cashFlowStatements": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/financialStatement"
          },
          "description": "An array of cash flow statements, showing the company's cash inflows and outflows over a specific period."
        }
      }
    },
    "mdAndA": {
      "type": "object",
      "description": "Management's Discussion and Analysis of financial condition and results of operations.",
      "properties": {
        "quantitativeAndQualitativeDisclosuresAboutMarketRisk": {
          "type": "string",
          "description": "Disclosures regarding market risk, including how it is managed."
        },
        "resultsOfOperations": {
          "type": "string",
          "description": "Management's perspective on the company's financial results and significant factors affecting them."
        },
        "liquidityAndCapitalResources": {
          "type": "string",
          "description": "An analysis of the company's liquidity and the condition of its capital resources."
        }
      }
    },
    "controlsAndProcedures": {
      "type": "string",
      "description": "Information on the company's controls and procedures, including internal control over financial reporting."
    },
    "riskFactors": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "A list of risk factors that could potentially affect the company's business, financial condition, or future results."
    }
  },
  "definitions": {
    "financialStatement": {
      "type": "object",
      "description": "A structure representing a single financial statement, such as a balance sheet, income statement, or cash flow statement.",
      "properties": {
        "title": {
          "type": "string",
          "description": "The title of the financial statement."
        },
        "periodEndDate": {
          "type": "string",
          "format": "date",
          "description": "The end date of the period covered by the financial statement."
        },
        "amounts": {
          "type": "object",
          "description": "A mapping of financial item names to their respective amounts, allowing for the representation of various financial metrics and figures.",
          "patternProperties": {
            "^[a-zA-Z ]+$": {
              "type": "number",
              "description": "The monetary value associated with the financial item, represented as a number."
            }
          }
        }
      },
      "required": ["title", "periodEndDate", "amounts"]
    }
  },
  "required": ["documentInfo", "financialStatements", "mdAndA"]
}
        """

        if 'schema' not in st.session_state:
            st.session_state['schema'] = default_schema.strip()

        with st.expander("Enter your JSON schema:", expanded=True):
            schema = st.text_area("JSON schema to be extracted:", value=st.session_state["schema"].strip(), height=500)

            st.session_state["schema"] = schema.strip()
            
            if schema:
                try:
                    st.caption("Formatted JSON schema:")

                    # Format the JSON input
                    formatted_json = json.dumps(json.loads(schema), indent=2)

                    st.code(formatted_json, language='json')
                except json.JSONDecodeError:
                    st.error("Invalid JSON schema.")

        submit_extract = st.button("Extract JSON")

        if submit_extract:
            if st.session_state['specification_id'] is not None:
                with st.spinner('Deleting existing specification... Please wait.'):
                    delete_specification()
                st.session_state["specification_id"] = None

            if st.session_state['specification_id'] is None:
                error_message = create_specification(st.session_state["schema"])

                if error_message is not None:
                    st.error(f"Failed to create specification. {error_message}")
                else:
                    start_time = time.time()

                    with st.spinner('Extracting JSON... Please wait.'):
                        response, error_message = extract_content()
                    
                        if error_message is not None:
                            st.error(f"Failed to extract JSON. {error_message}")

                        if response is not None:
                            st.subheader("Extracted JSON:")
                            st.json(response)
                        else:
                            st.text("No JSON was extracted.")

                        duration = time.time() - start_time

                        current_time = datetime.now()
                        formatted_time = current_time.strftime("%H:%M:%S")

                        st.success(f"JSON extraction took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Select a PDF, or fill in your own document URL.
        - **Step 3:** Enter JSON schema for data to be extracted.
        - **Step 4:** View JSON extracted from document text.
        """)

    with st.form("credentials_form"):
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