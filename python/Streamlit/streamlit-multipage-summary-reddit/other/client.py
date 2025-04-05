import streamlit as st
from typing import Optional, List
from graphlit import Graphlit
from graphlit_api import *

async def create_feed(name):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    input = FeedInput(
        name=name,
        type=FeedTypes.REDDIT,
        reddit=RedditFeedPropertiesInput(
            subredditName=name,
            readLimit=10
        )
    )

    try:
        response = await graphlit.client.create_feed(input)
        
        st.session_state['feed_id'] = response.create_feed.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def delete_feed():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_feed(st.session_state['feed_id'])

    st.session_state['feed_id'] = None
    st.session_state['feed_done'] = None

async def delete_all_feeds():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_feeds()

    st.session_state['feed_id'] = None
    st.session_state['feed_done'] = None

async def is_feed_done():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    response = await graphlit.client.is_feed_done(st.session_state['feed_id'])
    
    return response.is_feed_done.result

async def create_specification():
    input = SpecificationInput(
        name="Summarization",
        type=SpecificationTypes.COMPLETION,
        serviceType=ModelServiceTypes.ANTHROPIC,
        searchType=SearchTypes.VECTOR,
        anthropic=AnthropicModelPropertiesInput(
            model=AnthropicModels.CLAUDE_3_HAIKU,
            temperature=0.1,
            probability=0.2,
            completionTokenLimit=2048,
        )
    )

    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.create_specification(input)

        st.session_state['specification_id'] = response.create_specification.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def delete_specification():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_specification(st.session_state['specification_id'])

    st.session_state['specification_id'] = None

async def summarize_contents():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.summarize_contents(
            filter=ContentFilter(
                types=[ContentTypes.POST],
                feeds=[
                    EntityReferenceFilter(
                        id=st.session_state["feed_id"] 
                    )
                ]
            ),
            summarizations=[
                SummarizationStrategyInput(
                    type=SummarizationTypes.QUESTIONS,
                    specification=EntityReferenceInput(
                        id=st.session_state["specification_id"]
                    )
                )
            ]
        )

        if response.summarize_contents is None or response.summarize_contents.count == 0:
            return "No summary generated.", None

        return "\n\n".join(item.text for content in response.summarize_contents for item in content.items), None
    except GraphQLClientError as e:
        return None, str(e)