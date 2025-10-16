import asyncio
import sys
import traceback

from beeai_framework.adapters.a2a.serve.server import _react_agent_factory
from beeai_framework.agents.react import ReActAgent
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

logger = get_logger(__name__)
load_dotenv(dotenv_path=".secret")

async def main() -> None:
    # llm = ChatModel.from_name("gemini:gemini-2.5-flash")
    # agent = ReActAgent(
    #     llm=llm,
    #     tools=[DuckDuckGoSearchTool()],
    #     memory=UnconstrainedMemory(),
    # )

    system_prompt = """
        You are a very intelligent, smart financial analyst. You have great knowledge about stock market.
        Stock market is affected by mutliple factors like politics, international politics, weather, environment, 
        Socio-economic factors of the country, political stability of the country, allies of the country, political leadership,
        gold price, dollar price etc. These are just a few factors but majorly everything happening in the world impacts the stock market.

        You being a smart financial analyst, you need to have very good knowledge on the current affairs, 
        how the market has impacted in the past, which may help determine what can happen in future. 
        To serve the user query, you must refer to the websites like fool.com, finance.yahoo.com, wsj.com, google.com (donot just limit to these sites)
 
        After you analyze, you will provide the recommendations With all the details below 
        1. Name of the stock, current price, 2. % increase expected, Analyst ratings(buy,sell, hold how many),
         3. projection - 1 month, 4. projection - 3 month, 5. projection - 6 month,
         6. Reasons for the pojections,
         7. Most important news in last 3 months, Reference to sites you have reviewed

         Use all the tools provided to fetch the required information and show the final result
    """

    agent = RequirementAgent(
        llm=ChatModel.from_name("gemini:gemini-2.5-flash"),
        tools=[
            ThinkTool(),  # to reason
            DuckDuckGoSearchTool(),  # search web
            GoToURLTool(),
            ClickAtCoordinates(),
            FindElementWithText(),
            ClickElementWithText(),
            EnterTextIntoElement(),
            ScrollDownScreen(),
            GetPageSource(),
            AnalyzeWebpagAndDetermineAction()
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

    prompt ="""
        Provide me the top 10 AI stocks that are less than 10$.
    """
    response = await agent.run(system_prompt + prompt)

    print(f"Agent 🤖 :  {response.last_message.text}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())