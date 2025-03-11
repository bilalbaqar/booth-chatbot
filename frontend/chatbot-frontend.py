import streamlit as st
import requests
import json
from datetime import datetime

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Set the title using StreamLit
st.title('Booth Course Assistant')

# Display chat history
st.write('### Chat History')
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "raw_data" in message:
            with st.expander("Raw Response Data"):
                # Format the bot thinking with proper newlines
                if "bot_thinking" in message["raw_data"]:
                    thinking = message["raw_data"]["bot_thinking"]
                    # Split thinking into steps
                    steps = thinking.split("\n")
                    st.write("### Bot's Thinking Process:")
                    for step in steps:
                        if step.strip():
                            st.text(step.strip())
                # Display the rest of the raw data
                st.code(json.dumps(message["raw_data"], indent=2))

# Add a text input for the query
query = st.text_input('Ask a question about Booth courses:')

# Add a submit button
if st.button('Submit'):
    if query:
        try:
            # Add user query to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": query,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Send POST request to the Flask API
            response = requests.post(
                'http://127.0.0.1:5000/api/query',
                json={'query': query}
            )
            
            # Print raw response for debugging
            print("Raw Response:", response.text)
            print("Status Code:", response.status_code)
            
            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                print("Parsed JSON:", json.dumps(result, indent=2))
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result['response'],
                    "raw_data": result,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Display the response in a chat message
                with st.chat_message("assistant"):
                    st.write(result['response'])
                    with st.expander("See thinking and Raw Response Data"):
                        # Format the bot thinking with proper newlines
                        if "bot_thinking" in result:
                            thinking = result["bot_thinking"]
                            # Split thinking into steps
                            steps = thinking.split("\n")
                            st.write("### Bot's Thinking Process:")
                            for step in steps:
                                if step.strip():
                                    st.text(step.strip())
                        # Display the rest of the raw data
                        st.write("### Raw Response Data:")
                        st.code(json.dumps(result, indent=2))
                
                # Clear the input
                st.session_state.query = ""
                
            else:
                error_message = f'Error: {response.status_code} - {response.text}'
                st.error(error_message)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_message,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
        except requests.exceptions.ConnectionError:
            error_message = 'Could not connect to the server. Make sure the Flask server is running.'
            st.error(error_message)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            st.error(error_message)
            print(f"Exception details: {str(e)}")
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    else:
        st.warning('Please enter a query first.')

# Add a clear chat button
if st.button('Clear Chat History'):
    st.session_state.chat_history = []
    st.rerun()

# Add some helpful information
with st.expander('About this Assistant'):
    st.write("""
    This assistant can help you with:
    - Course information and prerequisites
    - Degree requirements
    - Concentration requirements
    - Course bidding history
    - Course syllabi
    """)