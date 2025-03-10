from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent
from langchain import hub
from langchain.agents import AgentExecutor

from dotenv import load_dotenv
load_dotenv()

from tools.degree_requirements import degree_requirements_checker
from tools.concentration_requirements import concentration_requirements_checker
from tools.course_csv_loaders.course_loader_context import course_tool_context_search
from tools.course_csv_loaders.course_loader_vector import course_tool_vector_search
from tools.course_csv_loaders.course_name_finder import course_to_title
from prompts.react_prompt import REACT_PROMPT

@tool
def get_weather(location: str):
    """Placeholder for getting weather."""
    if "San Francisco" in location:
        return "It's sunny in San Francisco."
    else:
        return f"Unknown weather in {location}"

@tool
def calculate_length(text: str):
    """Calculate the length of a given text."""
    return f"The text has {len(text)} characters."

@tool
def bidding_question(text: str):
    """Answer any questions related to bidding, bid points, course selection, etc."""
    return f"You can only take Microeconomics because that is the only course that is offered."


# Define the language model
llm = ChatOpenAI(model="gpt-4o-mini")

# course_tool = course_tool_context_search
course_tool = course_tool_vector_search

# Define the tools
tools = [degree_requirements_checker, concentration_requirements_checker, course_tool, course_to_title]

# Create the ReAct agent using the imported prompt
react_agent = create_react_agent(llm, tools, REACT_PROMPT)

# Create an executor for the agent
agent_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)

if __name__ == "__main__":
    decision = input("Do you want to ask questions? (y/n)")

    if decision.lower() == "y":
            print("📘 CSV Course Query Assistant")
            print("Type your questions about the course schedule. Type 'exit' to quit.\n")

            while True:
                # Get query input from the user
                query = input("Enter your query: ")

                # Exit condition
                if query.lower() == "exit":
                    print("Exiting the tool. Have a great day! 👋")
                    break

                result = agent_executor.invoke({"input": query})
                print(f"\nQuery: {query}")
                # Display the result
                print(f"\nResponse: {result}\n")
    else:
        test_queries = [
            "What is the title for 35150?",
            "Does 30131 fulfill requirements for Accounting concentration?",
            "What courses can I take to fulfill the Decisions requirement?",
            "What is the course number for investments?",
            "What are the course numbers for investments and financial accounting?"
            #"Give me 5 courses that are offered in Spring 2025?"
        ]

        for query in test_queries:
            print(f"\nQuery: {query}")
            result = agent_executor.invoke({"input": query})
            print(f"Response: {result}")


    
