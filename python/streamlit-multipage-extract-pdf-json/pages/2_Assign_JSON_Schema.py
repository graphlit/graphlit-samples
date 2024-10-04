import streamlit as st
import json
from other import client, helpers
from components import extract, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

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

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if 'schema' not in st.session_state:
            st.session_state['schema'] = default_schema.strip()

        if st.session_state['content_done'] == True:
            submit_extract = st.button("Extract JSON", key="submit_extract")

            if submit_extract:
                st.switch_page("pages/3_Extract_JSON.py")

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
        else:
            st.info("Please upload a file to extract.")   

    with col2:
        st.markdown("**Python SDK code example:**")
        
        with stylable_container(
            "codeblock",
            """
            code {
                white-space: pre-wrap !important;
            }
            """,
        ):
            st.code(language="python", body="""
                    from graphlit import Graphlit
                    from graphlit_api import *

                    input = SpecificationInput(
                        name="Extraction",
                        type=SpecificationTypes.EXTRACTION,
                        serviceType=ModelServiceTypes.OPEN_AI,
                        searchType=SearchTypes.VECTOR,
                        openAI=OpenAIModelPropertiesInput(
                            model=OpenAIModels.GPT4O_128K,
                            temperature=0.1,
                            probability=0.2,
                            completionTokenLimit=2048,
                        ),
                        tools=[
                            ToolDefinitionInput(
                                name="{name}",
                                schema="{schema}"
                            )
                        ]
                    )
                    
                    response = await graphlit.client.create_specification(input)

                    """)
