from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.callbacks.base import BaseCallbackHandler
from flask import Flask, request, jsonify
from flask_cors import CORS
import argparse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Import tools
from tools.degree_requirements import degree_requirements_checker
from tools.concentration_requirements import concentration_requirements_checker
from tools.course_csv_loaders.course_loader_context import course_tool_context_search
from tools.course_csv_loaders.course_loader_vector import course_tool_vector_search
from tools.course_csv_loaders.course_name_finder import course_to_title
from tools.syllabus_loader.syllabus_tool import syllabus_qa
from tools.bidding_loader.bidding_tool import bid_history_qa
from prompts.react_prompt import REACT_PROMPT

class CaptureThinkingCallback(BaseCallbackHandler):
    """Callback handler to capture the agent's thinking process."""
    
    def __init__(self):
        self.thinking_steps = []

    def on_chain_start(self, serialized, inputs, **kwargs):
        """Capture the start of a new chain with its inputs."""
        self.thinking_steps.append(f"Starting new invocation with input: {inputs}")

    def on_agent_action(self, action, **kwargs):
        """Capture each action the agent takes."""
        self.thinking_steps.append(f"Agent is thinking: {action}")

    def on_agent_finish(self, finish, **kwargs):
        """Capture the agent's final response."""
        self.thinking_steps.append(f"Final agent response: {finish}")

def setup_agent():
    """Initialize and configure the agent with all necessary components."""
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Initialize language model
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Define available tools
    tools = [
        degree_requirements_checker,
        concentration_requirements_checker,
        course_tool_vector_search,
        course_to_title,
        syllabus_qa,
        bid_history_qa
    ]

    # Initialize memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )

    # Create the ReAct agent
    react_agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=REACT_PROMPT,
        output_parser=ReActSingleInputOutputParser()
    )

    # Initialize thinking callback
    thinking_callback = CaptureThinkingCallback()

    # Create agent executor
    agent_executor = AgentExecutor(
        agent=react_agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=20,
        callbacks=[thinking_callback]
    )

    return app, agent_executor, thinking_callback

# Initialize components
app, agent_executor, thinking_callback = setup_agent()

@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Handle incoming queries and return responses using the agent.
    
    Expected JSON payload:
    {
        "query": "Your question here"
    }
    
    Returns:
        JSON response with the agent's answer and thinking process
    """
    try:
        # Validate request
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing query in request body'
            }), 400

        # Process query
        query = data['query']
        result = agent_executor.invoke({"input": query})
        bot_thinking = "\n".join(thinking_callback.thinking_steps)
        
        # Clear thinking steps for next query
        thinking_callback.thinking_steps = []

        return jsonify({
            'query': query,
            'response': result['output'],
            'bot_thinking': bot_thinking
        })

    except Exception as e:
        return jsonify({
            'error': f'Error processing query: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API status."""
    return jsonify({
        'status': 'healthy',
        'message': 'Booth Agent API is running'
    })

def run_cli():
    """Run the agent in interactive CLI mode."""
    print("📘 CSV Course Query Assistant")
    print("Type your questions about the course schedule. Type 'exit' to quit.\n")
    print("I'll remember our conversation to provide better context for your questions.\n")

    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit":
            print("Exiting the tool. Have a great day! 👋")
            break

        result = agent_executor.invoke({"input": query})
        print(f"\nQuery: {query}")
        print(f"\nResponse: {result['output']}\n")

def run_tests():
    """Run predefined test queries to verify agent functionality."""
    test_queries = [
        "What is the title for 35150?",
        "Does 30131 fulfill requirements for Accounting concentration?",
        "What courses can I take to fulfill the Decisions requirement?",
        "What is the course number for investments?",
        "What are the course numbers for investments and financial accounting?",
        "What are the prerequisites for Advanced Investments?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = agent_executor.invoke({"input": query})
        print(f"Response: {result['output']}")

def run_server():
    """Run the Flask server with the specified configuration."""
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Booth Agent - Course Query Assistant')
    parser.add_argument('--server', action='store_true', help='Run as Flask server')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--test', action='store_true', help='Run test queries')
    
    args = parser.parse_args()
    
    # Execute the appropriate mode based on arguments
    if args.server:
        run_server()
    elif args.cli:
        run_cli()
    elif args.test:
        run_tests()
    else:
        parser.print_help()


    
