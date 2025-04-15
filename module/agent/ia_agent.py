import os
from langchain_core.messages import AIMessage

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv


load_dotenv()


client = MultiServerMCPClient({
    "test": {
            "url": "http://localhost:8000/mcp",
        },
})


model  = ChatOpenAI(
    model="gpt-4o-mini",
    api_key = os.getenv("OPENAI_API_KEY"),
    
    temperature=0,
    )


async def agent_loop():
    async with MultiServerMCPClient(
        {
            "test": {
                "url": "http://localhost:8000/mcp",
                "transport": "sse",
            },
        }
    ) as client:
        tools = client.get_tools()
        # for tool in tools:
        #     print(tool.name, tool.description)
            
        agent = create_react_agent(model, tools)

        while True:
            user_input = input("Digite sua mensagem: ")
            response = await agent.ainvoke({"messages": user_input})
            
            for message in response['messages'][1:]:
                print(message.content)
            