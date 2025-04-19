import os
import logging


from typing import List
from langchain_core.messages import BaseMessage
from langchain_core.messages import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv


load_dotenv()


client = MultiServerMCPClient({
    "items": {
            "url": "http://localhost:8000/mcp",
            "transport": "sse",
        },
})


model  = ChatOpenAI(
    model="gpt-4o-mini",
    api_key = os.getenv("OPENAI_API_KEY"),
    
    temperature=0,
    )

async def process_agent_messages(messages: List[BaseMessage]):
    async with client:
        tools = client.get_tools()
        agent = create_react_agent(
            model,
            tools=tools,
            version="v2",
        )
        response = await agent.ainvoke({"messages": messages})
        return response["messages"]

async def agent_test_loop():
    history = []
    
    async with client:
        tools = client.get_tools()
        
        for tool in tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            print("-" * 20)
        
        agent = create_react_agent(
            model,
            tools=tools,
            # debug=True,
            # version="v1",
            version="v2",
            )

        while True:
            user_input = input("Digite sua mensagem: ")
            
            history.append(HumanMessage(content=user_input))
            
            response = await agent.ainvoke({"messages": history})
            
            ai_response = response["messages"][-1]
            print(ai_response.content)
            history.append(ai_response)
            