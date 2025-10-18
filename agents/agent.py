import asyncio
import sys
import traceback

from beeai_framework.adapters.a2a.serve.server import _react_agent_factory

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.errors import FrameworkError
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.agents.requirement.requirements.conditional import (
    ConditionalRequirement,
)

from util.logger import get_logger
from dotenv import load_dotenv
from tools.web_crawler import (
    AnalyzeWebpagAndDetermineAction,ClickAtCoordinates,ClickElementWithText,EnterTextIntoElement,
    FindElementWithText,GetPageSource,GoToURLTool,ScrollDownScreen
    )
from rag.chroma_tool import ChromaRetrieverTool

logger = get_logger(__name__)
load_dotenv(dotenv_path=".secret")

def getAgent() -> RequirementAgent:
    # llm = ChatModel.from_name("gemini:gemini-2.5-flash")
    # agent = ReActAgent(
    #     llm=llm,
    #     tools=[DuckDuckGoSearchTool()],
    #     memory=UnconstrainedMemory(),
    # )

    system_prompt = """
        provide the stock details as per the US market
        """
    
    agent = RequirementAgent(
        llm=ChatModel.from_name("gemini:gemini-2.5-flash"),
        tools=[
            ThinkTool(),  # to reason
            DuckDuckGoSearchTool(),  # search web
            ChromaRetrieverTool() # Retrieve the internal stock research 
        ],
        memory=UnconstrainedMemory(),
        instructions=system_prompt,
        requirements=[
            # Search only after getting weather and at least once
            ConditionalRequirement(DuckDuckGoSearchTool, force_at_step=1,max_invocations=5),
            # Force thinking first
            ConditionalRequirement(ThinkTool, only_after=[DuckDuckGoSearchTool], min_invocations=1,max_invocations=5),
        ],
    )
    agent.allow_parallel_tool_calls = True

    return agent