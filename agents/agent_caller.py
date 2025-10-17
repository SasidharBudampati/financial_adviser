import asyncio
import sys
import traceback

from beeai_framework.adapters.a2a.serve.server import _react_agent_factory
from beeai_framework.adapters.a2a.agents import A2AAgent, A2AAgentUpdateEvent

from beeai_framework.agents.requirement import RequirementAgent

from beeai_framework.memory import UnconstrainedMemory

from beeai_framework.errors import FrameworkError

from examples.helpers.io import ConsoleReader
from util.logger import get_logger
from dotenv import load_dotenv

from beeai_framework.emitter import EventMeta

logger = get_logger(__name__)
load_dotenv(dotenv_path=".secret")

async def main() -> RequirementAgent:
    await getAgent()

async def getAgent() -> RequirementAgent:
    
    agent = A2AAgent(url="http://127.0.0.1:9999", memory=UnconstrainedMemory())
    agent.allow_parallel_tool_calls = True
    reader = ConsoleReader()
    for prompt in reader:
        # Run the agent and observe events
        def print_update(data: A2AAgentUpdateEvent, event: EventMeta) -> None:
            value = data.value
            debug_info = value[1] if isinstance(value, tuple) else value
            reader.write("Agent 🤖 (debug) : ", str(debug_info))

        response = await agent.run(prompt).on("update", print_update)

        reader.write("Agent 🤖 : ", response.last_message.text)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())