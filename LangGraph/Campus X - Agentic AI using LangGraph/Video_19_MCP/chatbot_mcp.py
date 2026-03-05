from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import requests
import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()
os.environ['LANGCHAIN_PROJECT']='MCP-Chatbot-LangSmith'

# 1. LLM
# -------------------
llm = ChatOpenAI(model="gpt-4o-mini")

# MCP client for local FastMCP server
client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio", #as the mcp is in our local
            "command": "python",
            "args": ["D:/Ankit/Generative AI/LangGraph/Campus X - Agentic AI using LangGraph/Video_19_MCP/main.py"],
        },
        "expense": { #this tool adds expense, shows expence, etc. If you want to achieve it via tools then you need to make a separate tool for each functionaly whereas MCP lets you do it in one go
            "transport": "streamable_http",  # if this fails, try "sse"
            "url": "https://splendid-gold-dingo.fastmcp.app/mcp" #an mcp server of Nitish Campus X
        }
    }
)


#state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

async def build_graph():
    
    tools = await client.get_tools() #this fetches all tools in the mcp server

    print(tools)
    print("=====================================================================")

    llm_with_tools = llm.bind_tools(tools)

    # To make LangGraph asynchronous, you have to make their nodes async
    # 4. Nodes
    async def chat_node(state: ChatState):
        """LLM node that may answer or request a tool call."""
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Tool node is built async internally so we don't have to explicitely make it async
    tool_node = ToolNode(tools)

    # -------------------
    # 6. Graph
    # -------------------
    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")

    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge('tools', 'chat_node')

    chatbot = graph.compile()

    return chatbot

async def main():

    chatbot = await build_graph()

    #running the graph | we are doing asynchronous invoke
    # result = await chatbot.ainvoke({"messages": [HumanMessage(content="Find the modulus of 132354 and 23 "
    # "and give answer like a cricket commentator")]})

    result = await chatbot.ainvoke({"messages": [HumanMessage(content="Add an expense - Rs 200 for a udemy course on 10th Nov")]})

    print(result['messages'][-1].content)

if __name__ == '__main__':
    asyncio.run(main())
