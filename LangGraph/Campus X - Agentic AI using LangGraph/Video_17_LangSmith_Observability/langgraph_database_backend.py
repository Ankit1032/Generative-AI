# pip install langgraph-checkpoint-sqlite <--do this

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3 #to create sqlite database

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# chatbot.db will get created if it doesn't exist already
# As Sqlite only works on same thread, we have to explicitely mention check_same_thread=False.
# This tells sqlite that we will work on multiple threads.
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# Checkpointer
checkpointer = SqliteSaver(conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# test
# CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# response = chatbot.invoke(
#     {'messages': [HumanMessage(content='Hi my name is Ankit')]},
#     config=CONFIG
# )

####OUTPUT:
# [HumanMessage(content='Hi my name is Ankit', additional_kwargs={}, response_metadata={}, id='c3dcbfaf-82dd-4710-8d10-ac931cfcbf5d'), 
# # AIMessage(content='Hi Ankit! How can I assist you today?' ....

# to prove that the previous response was stored in sqlite -> chatbot.db
# we will ask the LLM -> what is my name

# response = chatbot.invoke(
#     {'messages': [HumanMessage(content='What is my name?')]},
#     config=CONFIG
# )

## OUTPUT: AIMessage(content='Your name is Ankit. How can I help you today?'

## If you change config thread and rerun your prompts, you will see that sqlite is
# able to store conversation in each thread as well.


# print(response)

# to check your chatbot.db, go to VS code extension --> sqlite viewer --> once installed
# --> click on db

# CONFIG = {'configurable': {'thread_id': 'thread-2'}}
# response = chatbot.invoke(
#     {'messages': [HumanMessage(content='What is my name')]},
#     config=CONFIG
# )
# print(response)

#OUTPUT: It failed to say my name as this thread is different from where my name is  stored

# FInd out the list of all the overall checkpoints
# it can also give me list of checkpoints for a particular thread
# sending parameter None meaning we need list of all checkpoints, not for any thread
# for checkpoint in checkpointer.list(None): # to print list of all checkpoints
#     print(checkpoint)

#we need to store unique threads so we will use sets

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)