import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid # to create random thread id

user_input = st.chat_input("Type here")

# ************************* Utility Functions ************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

# Storing all multiple threads in chat_threads
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# Provide thread_id and it returns list of all the messages and responses.
# def load_conversation(thread_id):
#     return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
# this function also makes sure if u make a new chat and hop onto another chat and then revisit that 'new chat', it shouldn't throw any error.
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    
    if not state or 'messages' not in state.values:
        return []
    
    return state.values['messages']
# ************************* Session Setup ****************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

# ************************* Sidebar UI *************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My conversations')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)): #if thread button is clicked then load that conversation by passing that thread
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id) #in return, we will receive list of messages
        
        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'

            temp_messages.append({'role':role, 'content': msg.content})
        
        st.session_state['message_history'] = temp_messages
# ************************* Main UI ****************************

#loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

if user_input:

    # first add the message to message history
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message("user"):
        st.text(user_input)

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode = 'messages'
            )
        )

    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})