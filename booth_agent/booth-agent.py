from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent
from langchain import hub
from langchain.agents import AgentExecutor

from dotenv import load_dotenv
load_dotenv()

from tools.degree_requirements import degree_requirements_checker
from tools.course_csv_loaders.csv_qa import csv_question_answerer
from tools.course_csv_loaders.course_info import csv_vector_search

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

#course_tool = csv_question_answerer
course_tool = csv_vector_search

# Define the tools
tools = [degree_requirements_checker, course_tool]

# Pull a ReAct prompt template
prompt = hub.pull("hwchase17/react")

# Create the ReAct agent
react_agent = create_react_agent(llm, tools, prompt)




# Create an executor for the agent
agent_executor = AgentExecutor(agent=react_agent, tools=tools)

# Execute the agent with an input
#result = agent_executor.invoke({"input": "What courses can I take to fulfill the Decisions requirement?"})

#print(result)





if __name__ == "__main__":
    test_queries = [
        "What courses can I take to fulfill the Decisions requirement?",
        "What is the course number for investments?",
        "What are the course numbers for investments and financial accounting?",
        "Give me 5 courses that are offered in Spring 2025?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = agent_executor.invoke({"input": query})
        print(f"Response: {result}")
    
    exit()


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
