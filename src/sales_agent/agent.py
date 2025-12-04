from google.adk.agents.llm_agent import Agent
from .sub_agents.pricing_calculator import pricing_calculator_agent
from .sub_agents.competitor_analyst import competitor_analyst_agent
from .sub_agents.interview_analyzer import interview_analyzer_agent
from .sub_agents.product_matcher import product_matcher_agent
from .sub_agents.proposal_writer import proposal_writer_agent
from .sub_agents.visual_generator import visual_generator_agent
from .sub_agents.docx_assembler import docx_assembler_agent
from google.adk.tools import agent_tool

instruction = """You are the Lead Project Manager for a proposal generation system.
        Your goal is to orchestrate a team of specialized AI agents to build a Comarch sales proposal.

        **Workflow Management:**
        You must trigger the sub-agents or tools in the following strict order. Pass the output of one phase as context to the next.

        1.  **Analysis Phase:** Send user input to the interview_analyzer to get a structured client profile.
        2.  **Strategy Phase:** Once the profile is ready, trigger product_matcher AND competitor_analyst (simultaneously if possible).
        3.  **Pricing Phase:** Pass the selected products to the pricing_calculator.
        4.  **Creation Phase:** Provide all accumulated data to the proposal_writer (for text) and visual_generator (for assets).
        5.  **Assembly Phase:** Finally, use docx_assembler to combine the proposal text and generated images into a final DOCX document.

        **Constraints:**
        Do not generate the final proposal content yourself.
        If a sub-agent or tool returns incomplete data, flag it for human review."""



competitor_analyst_as_tool = agent_tool.AgentTool(agent=competitor_analyst_agent)
interview_analyzer_as_tool = agent_tool.AgentTool(agent=interview_analyzer_agent)
proposal_writer_as_tool = agent_tool.AgentTool(agent=proposal_writer_agent)
pricing_calculator_as_tool = agent_tool.AgentTool(agent=pricing_calculator_agent)
product_matcher_as_tool = agent_tool.AgentTool(agent=product_matcher_agent)
visual_generator_agent_as_tool = agent_tool.AgentTool(agent=visual_generator_agent)
docx_assembler_as_tool = agent_tool.AgentTool(agent=docx_assembler_agent)

orchestrator_agent  = Agent(
    model='gemini-2.5-flash',
    name="orchestrator",
    description="Project Manager responsible for coordinating the proposal generation workflow.",
    instruction = instruction,
    tools = [
        interview_analyzer_as_tool,
        product_matcher_as_tool,
        competitor_analyst_as_tool,
        pricing_calculator_as_tool,
        proposal_writer_as_tool,
        visual_generator_agent_as_tool,
        docx_assembler_as_tool
    ]
)

root_agent = orchestrator_agent
