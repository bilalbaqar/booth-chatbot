import pandas as pd
from langchain_core.tools import tool, Tool
from pathlib import Path
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


# Initialize file paths
current_file = Path(__file__)
BASE_DIR = current_file.parents[3]
FILE_PATH = BASE_DIR / "data" / "bidding-history.csv"

# Initialize bidding data at module level
try:
    bidding_data = pd.read_csv(FILE_PATH)
    print(f"Successfully loaded bidding data from {FILE_PATH}")
    print(f"Total records: {len(bidding_data)}")
except FileNotFoundError:
    print(f"Warning: Bidding history file not found at {FILE_PATH}")
    print("Please run the bidding_history_loader.py script first")
    bidding_data = None
except Exception as e:
    print(f"Error loading bidding data: {str(e)}")
    bidding_data = None


@tool("bid_history_by_course_number")
def bid_history_by_course_number(course_number: str) -> str:
    """
    Retrieve bid point history for a given Booth course.
    
    Args:
        course_number: The course number (e.g., "30000")
    
    Returns:
        Formatted string containing bid history details with quarter-year and prices for each phase.
    """
    if bidding_data is None:
        return "Error: Bidding data not initialized. Please ensure the bidding history CSV file exists and is properly formatted."

    filtered_data = bidding_data[bidding_data["Course_Number"].astype(str) == course_number].copy()

    if filtered_data.empty:
        return f"No bid history found for course {course_number}"

    # Create quarter-year column
    filtered_data['Quarter-Year'] = filtered_data['Quarter'] + '-' + filtered_data['Year'].astype(str)
    
    # Select only needed columns
    columns_needed = ['Quarter-Year', 'Phase 1 Price', 'Phase 2 Price', 'Phase 3 Price']
    
    # Group by Quarter-Year and take the first section's data for each quarter
    simplified_data = (filtered_data[columns_needed]
                      .groupby('Quarter-Year')
                      .first()
                      .reset_index()
                      .sort_values('Quarter-Year', ascending=False))
    
    # Get course info
    course_info = filtered_data.iloc[0]
    
    # Create formatted output string
    output = f"Course: {course_number} - {course_info['Title']}\n\nBid History by Quarter:\n"
    
    for _, row in simplified_data.iterrows():
        output += f"\n{row['Quarter-Year']}:"
        output += f"\n  Phase 1: {row['Phase 1 Price']} points"
        output += f"\n  Phase 2: {row['Phase 2 Price']} points"
        output += f"\n  Phase 3: {row['Phase 3 Price']} points" if not pd.isna(row['Phase 3 Price']) else "\n  Phase 3: No data"
    
    print(output)
    return output

REACT_PROMPT = PromptTemplate.from_template(
    """You are a Booth School of Business bidding assistant that helps students determine optimal bid points for courses. 
    You have access to bid_history_by_course_number tool which retrieves bid point history for a given Booth course. The tool returns a formatted string with the course information and bid history by quarter.

    {tools}

    Current question: {input}

    Use the following format:

    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Important Instructions for Bid Analysis:
    1. If only a course name is provided (without a course number):
       - Respond with "To provide accurate bidding information, I need the course number. Please provide the course number for [course name]."
       
    2. When analyzing bid history:
       - Look at the bid points across different quarters
       - Note any patterns in Phase 1 vs Phase 2 vs Phase 3 prices
       - Highlight quarters with unusually high or low bid points
       - Consider recent trends in bid points
       
    3. When providing recommendations:
       - Start with the course name and number
       - Provide specific bid point ranges for each phase
       - Mention any recent trends
       - Note if the course typically requires points or is usually available without points


    4. You will not make up any information. You will only use the information provided by the bid_history_by_course_number tool.

    Begin!
    
    Thought: {agent_scratchpad}"""
)


# Create the tools list with properly decorated function
tools = [bid_history_by_course_number]

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create the ReAct agent using the imported prompt
react_agent = create_react_agent(llm, tools, REACT_PROMPT)

# Create an executor for the agent
agent_executor = AgentExecutor(
    agent=react_agent,
    tools=tools, 
    handle_parsing_errors=True,
    verbose=True)

@tool("bid_history_qa")
def bid_history_qa(query: str) -> dict:
    """
    Answer questions about course bid points and history.
    
    Args:
        query: A question about course bidding history or strategy
        
    Returns:
        Detailed analysis of bid history and recommendations
    """
    result = agent_executor.invoke({"input": query})
    return result
    #return result["output"] if isinstance(result, dict) and "output" in result else result


if __name__ == "__main__":
    # Test the direct tool
    print("\nTesting direct bid history lookup:")
    print(bid_history_by_course_number("37202"))
    #print(bid_history_by_course_number("Pricing Strategies"))
    
    # Test the QA interface
    print("\nTesting bid history QA:")
    print(bid_history_qa("Give me the bid history for 37202?"))