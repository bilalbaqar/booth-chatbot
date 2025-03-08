from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent
from langchain import hub
from langchain.agents import AgentExecutor
from typing import Dict, List
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini"
)

# Define the degree requirements
DEGREE_REQUIREMENTS = """
Here are the degree requirements for MBA at Booth School of Business. You have to take 1 course each for the following:

Financial Accounting: 30000, 30116, 30120, 30122, 30130, 30131
Microeconomics: 33001, 33002, or 33101, ECON 30100, ECON 30200
Statistics: 41000 or 41100, 41201, 41202, 41203, 41204, 41206, 41207, 41301, 41305, 41813, 41814, 41901, 41902, 41903, 41910, 41916
"""

# Create the prompt template
COURSE_PLANNER_PROMPT = PromptTemplate.from_template(
    """You are a course planning assistant for the Booth School of Business MBA program. 
    Use the following degree requirements to help students plan their courses:

    {degree_requirements}

    When recommending courses, consider:
    1. The specific course requirements listed above
    2. The student's preferences and constraints (if provided)
    3. The quarter in which the student wants to take the course
    4. Any prerequisites or course restrictions

    Student's question: {query}

    Provide a detailed response that:
    1. Directly answers the student's question
    2. Lists specific course numbers and names that satisfy the requirements
    3. Explains why these courses are recommended
    4. Includes any relevant prerequisites or important notes

    Response:"""
)

def create_course_planner_tool() -> Tool:
    """
    Creates a course planning tool that uses an LLM to provide course recommendations.
    
    Returns:
        Tool: A LangChain Tool that can be used to plan courses
    """
    def course_planner(query: str) -> str:
        """
        A course planning tool for students at the Booth School of Business to help them plan their courses.
        
        Args:
            query (str): The student's question about course planning
            
        Returns:
            str: A detailed response with course recommendations
        """
        try:
            # Generate the prompt with the student's query
            prompt = COURSE_PLANNER_PROMPT.format(
                degree_requirements=DEGREE_REQUIREMENTS,
                query=query
            )
            
            # Get response from the LLM
            response = llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            return f"Error in course planning: {str(e)}"

    return Tool(
        name="Course Planner",
        func=course_planner,
        description="""A course planning tool for Booth MBA students that helps with:
        - Identifying courses that fulfill degree requirements
        - Recommending courses based on student preferences
        - Providing course information and prerequisites
        - Planning courses across different quarters
        Input should be a question about course planning or requirements."""
    )

# Example usage
if __name__ == "__main__":
    # Create the course planner tool
    course_planner_tool = create_course_planner_tool()
    
    # Example queries to test the tool
    test_queries = [
        "What courses can I take to fulfill the Financial Accounting requirement?",
        "I need to take Microeconomics next quarter. What are my options?",
        "Which Statistics courses are available for the MBA program?"
    ]
    
    # Test the tool with each query
    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {course_planner_tool.func(query)}")