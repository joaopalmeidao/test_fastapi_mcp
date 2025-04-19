from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Literal
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from module.agent.ia_agent import process_agent_messages

router = APIRouter()

# Modelo para entrada de mensagens
class MessageModel(BaseModel):
    type: Literal["human", "ia"] = Field(description="Tipo de mensagem: 'human' ou 'ia'")
    content: str = Field(description="Conteúdo da mensagem")

@router.post("/agent", response_model=str, tags=["agent"], operation_id="call_agent")
async def call_agent(messages: List[MessageModel]):
    history: List[BaseMessage] = []

    for msg in messages:
        if msg.type == "human":
            history.append(HumanMessage(content=msg.content))
        elif msg.type == "ai":
            history.append(AIMessage(content=msg.content))
        else:
            return {"error": f"Tipo de mensagem inválido: {msg.type}"}

    response_messages = await process_agent_messages(history)
    return response_messages[-1].content
