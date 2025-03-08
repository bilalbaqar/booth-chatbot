from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent
from langchain import hub
from langchain.agents import AgentExecutor

from dotenv import load_dotenv
load_dotenv()

from tools.degree_requirements import degree_requirements_checker

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

@tool
def course_planner(text: str):
    """
    A course planning tool for students at the Booth School of Business to help them plan their courses for the upcoming quarters.

    This tool provides the following functionalities:
    - Identifies which courses are being offered in the upcoming Fall, Winter, Spring, or Summer quarters.
    - Helps students fulfill degree requirements by suggesting eligible courses.
    - Assists in meeting concentration/specialization requirements by recommending relevant courses.
    - Allows students to input preferences such as preferred instructors, class formats (in-person/online), 
      and scheduling constraints.
    - Ensures students stay on track for graduation by balancing core, elective, and specialization courses.
    """
    return f"Take Microeconomics, it will cover all your requirements."




# Define the language model
llm = ChatOpenAI(model="gpt-4o-mini")

# Define the tools
tools = [get_weather, calculate_length, bidding_question, degree_requirements_checker]

# Pull a ReAct prompt template
prompt = hub.pull("hwchase17/react")

# Create the ReAct agent
react_agent = create_react_agent(llm, tools, prompt)




# Create an executor for the agent
agent_executor = AgentExecutor(agent=react_agent, tools=tools)

# Execute the agent with an input
result = agent_executor.invoke({"input": "What courses can I take to fulfill the Decisions requirement?"})

print(result)

