import streamlit as st
import requests
import json


# Set the title using StreamLit
st.title('Booth Course Assistant')

# Add a text input for the query
query = st.text_input('Ask a question about Booth courses:')

# Add a submit button
if st.button('Submit'):
    if query:
        try:
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
                
                st.write('### Response:')
                st.write(result['response'])
                
                # Display raw response in an expander
                with st.expander('Raw Response Data'):
                    st.code(json.dumps(result, indent=2))
            else:
                st.error(f'Error: {response.status_code} - {response.text}')
                
        except requests.exceptions.ConnectionError:
            st.error('Could not connect to the server. Make sure the Flask server is running.')
        except Exception as e:
            st.error(f'An error occurred: {str(e)}')
            print(f"Exception details: {str(e)}")
    else:
        st.warning('Please enter a query first.')

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