
import streamlit as st
from langgraph_tool_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid # to create random thread id

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
    st.session_state['chat_threads'] = retrieve_all_threads()

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

# CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

user_input = st.chat_input("Type here")

if user_input:

    # first add the message to message history
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message("user"):
        st.text(user_input)


    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",
    }

    with st.chat_message("assistant"):
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Tool status handling
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")

                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream only assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        # 👇 CALL THE STREAM OUTSIDE THE FUNCTION
        ai_message = st.write_stream(ai_only_stream())

        # Finalize tool status
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished",
                state="complete",
                expanded=False,
            )

    # 👇 Save assistant message OUTSIDE the with block
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )


# if user_input:

#     # first add the message to message history
#     st.session_state['message_history'].append({'role':'user', 'content':user_input})
#     with st.chat_message("user"):
#         st.text(user_input)

#     # first add the message to message_history
#     # we initially hit a problem where the LLM was printing the tool message along with 
#     # the chat message. to fix this(we dont wnt to see tool message),
#     # we wrote the below logic.
#     with st.chat_message("assistant"):
#         def ai_only_stream():
#             for message_chunk, metadata in chatbot.stream(
#                 {"messages": [HumanMessage(content=user_input)]},
#                 config=CONFIG,
#                 stream_mode="messages"
#             ):
#                 if isinstance(message_chunk, AIMessage): #stream only if it is AI message.
#                     # yield only assistant tokens
#                     yield message_chunk.content

#         ai_message = st.write_stream(ai_only_stream())

#     st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})