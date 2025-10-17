import asyncio
import sys
import traceback

from beeai_framework.adapters.a2a import A2AServer, A2AServerConfig
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.serve.utils import LRUMemoryManager
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.errors import FrameworkError

from agents.agent import getAgent

def main() -> None:

    agent1 = getAgent()

    A2AServer(
        config=A2AServerConfig(port=9999, protocol="jsonrpc"), memory_manager=LRUMemoryManager(maxsize=100)
    ).register(agent1, send_trajectory=True).serve()


if __name__ == "__main__":
    main()