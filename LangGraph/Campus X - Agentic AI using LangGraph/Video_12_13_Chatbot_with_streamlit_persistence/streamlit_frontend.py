import streamlit as st

##### BASICS #####
# with st.chat_message('user'):
#     st.text('Hi')

# with st.chat_message('assistant'):
#     st.text('How can I help you?')

# with st.chat_message('user'):
#     st.text('My name is Ankit')

# user_input = st.chat_input('Type here')

# if user_input:
#     with st.chat_message('user'):
#         st.text(user_input)

################################

##### Building a dumb chatbot where whatever USer writes, Assitant writes back
# Note: It doesn't keep adding texts to your UI so when you write new text, the whole streamlit code reruns from top to bottom 
# and it replaces the old text 

# user_input = st.chat_input("Type here")

# if user_input:

#     with st.chat_message("user"):
#         st.text(user_input)

#     with st.chat_message("assistant"):
#         st.text(user_input)

## So we need to create a dictionaryto store previous conversation #####
# user_input = st.chat_input("Type here")
# message_history: list

# for message in message_history:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# if user_input:

#     # first add the message to message history
#     message_history.append({'role':'user', 'content':user_input})
#     with st.chat_message("user"):
#         st.text(user_input)

#     # first add the message to message history
#     message_history.append({'role':'assistant', 'content':user_input})
#     with st.chat_message("assistant"):
#         st.text(user_input)

# It still won't run because whenever user writes a chat, the whole streamlit runs so 
#messahe_history keeps gettingre-initialized hence gets empty

# Streamlit has a global dictionary called st.session_state. 
# It won't erase even if the streamlit code reruns (clicking on rerun in streamlit UI)
# It will only reset if you refresh the page manually.

# user_input = st.chat_input("Type here")

# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []

# for message in st.session_state['message_history']:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# if user_input:

#     # first add the message to message history
#     st.session_state['message_history'].append({'role':'user', 'content':user_input})
#     with st.chat_message("user"):
#         st.text(user_input)

#     # first add the message to message history
#     st.session_state['message_history'].append({'role':'assistant', 'content':user_input})
#     with st.chat_message("assistant"):
#         st.text(user_input)

####### Now we will connect our backend to our frontend where role is assistant

from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread_1'}}

user_input = st.chat_input("Type here")

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

if user_input:

    # first add the message to message history
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message("user"):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response['messages'][-1].content

    # first add the message to message history
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)