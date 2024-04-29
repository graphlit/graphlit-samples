import streamlit as st
from typing import Optional
from graphlit import Graphlit
from graphlit_api import *

async def create_feed(owner, name, token):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    input = FeedInput(
        name=f"{owner}: {name}",
        type=FeedTypes.ISSUE,
        issue=IssueFeedPropertiesInput(
            type=FeedServiceTypes.GIT_HUB_ISSUES,
            github=GitHubIssuesFeedPropertiesInput(
                repositoryOwner=owner,
                repositoryName=name,
                personalAccessToken=token,
            ),
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
        name="Completion",
        type=SpecificationTypes.COMPLETION,
        serviceType=ModelServiceTypes.ANTHROPIC,
        searchType=SearchTypes.VECTOR,
        anthropic=AnthropicModelPropertiesInput(
            model=AnthropicModels.CLAUDE_3_HAIKU,
            temperature=0.1,
            probability=0.2,
            completionTokenLimit=2048,
        ),
        promptStrategy=PromptStrategyInput(
            type=PromptStrategyTypes.OPTIMIZE_SEARCH
        ),
        retrievalStrategy=RetrievalStrategyInput(
            type=RetrievalStrategyTypes.SECTION
        ),
        rerankingStrategy=RerankingStrategyInput(
            serviceType=RerankingModelServiceTypes.COHERE
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

async def publish_contents(prompt):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.publish_contents(
            connector=ContentPublishingConnectorInput(
                type=ContentPublishingServiceTypes.TEXT,
                format=ContentPublishingFormats.MARKDOWN
            ),
            publish_prompt=prompt,
            summary_specification=EntityReferenceInput(
                id=st.session_state["specification_id"]
            ),
            publish_specification=EntityReferenceInput(
                id=st.session_state["specification_id"]
            ),
            filter=ContentFilter(
                types=[FeedTypes.ISSUE],
                feeds=[
                    EntityReferenceFilter(
                     id=st.session_state['feed_id']
                    )
                ]
            ),
        )

        if response.publish_contents is None:
            return None, None
        
        return response.publish_contents.markdown, None
    except GraphQLClientError as e:
        return None, str(e)
