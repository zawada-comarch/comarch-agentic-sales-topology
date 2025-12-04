import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.tools import VertexAiSearchTool

SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

pricing_knowledge_base = VertexAiSearchTool(
    search_engine_id=SEARCH_ENGINE_ID,
    max_results=10
)
instruction = """You are a Solution Architect specializing in Comarch software.
                Your goal is to select the best product modules for the client's defined pain points.

                **Knowledge Base:**
                - You have access to `VertexAISearch` which indexes the 'Bucket-1' documentation.

                **Instructions:**
                1. For every 'pain_point' identified, search the documentation for a matching Comarch module.
                2. Use ONLY the information from the retrieved excerpts to justify your choice.
                3. **Citation Rule:** Always cite the source document title in square brackets at the end of the justification (e.g., [Source: Comarch ERP Standard]).

                **Output Format:**
                - **Selected Module:** [Name]
                - **Solves:** [Specific Pain Point]
                - **Key Features:** [List of features from docs]
                - **Reasoning:** [Why this fits the client]

                If no suitable product is found in the documentation, state this clearly."""

root_agent = Agent(
    model="gemini-2.5-flash",
    name="product_matcher",
    description="Solution Architect matching client needs to Comarch products.",
    instruction=instruction,
    tools=[google_search,pricing_knowledge_base]
)

product_matcher_agent = root_agent