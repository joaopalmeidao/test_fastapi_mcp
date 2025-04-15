import asyncio

from module.agent.ia_agent import agent_loop


if __name__ == "__main__":
    asyncio.run(agent_loop())