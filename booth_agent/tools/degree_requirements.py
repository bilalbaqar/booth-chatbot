from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini"
)

# Define the degree requirements
DEGREE_REQUIREMENTS = """
Here are the degree requirements for MBA at Booth School of Business. 


You have to take 1 course each for the following:

Financial Accounting: 30000, 30116, 30120, 30122, 30130, 30131
Microeconomics: 33001, 33002, or 33101, ECON 30100, ECON 30200
Statistics: 41000 or 41100, 41201, 41202, 41203, 41204, 41206, 41207, 41301, 41305, 41813, 41814, 41901, 41902, 41903, 41910, 41916

Select one each from seven of the following eight:

Finance	35000, 35001, or 35200	 34101, 34901, 34902, 34903, 34904, 35100, 35120, 35130, 35150, 35201, 35210, 35214
Marketing	37000 or 37110	37101, 37103, 37105, 37106, 37107, 37200, 37201,37202, 37208, 37209, 37110, 37301, 37304, 37703, 37704 
Operations	40000	40101, 40108, 40110
Strategy	42001	39001, 39101, 42116, 42135, 42715	
Decisions	30005 (or 30001), 36106, or 38002, 38120 36109
People	33032, 38001, 38003, or 39002 31403, 38122	 	
Economy	33050 (or 33040) or 33112	33401, 33403, 33501, 33502, 33503, 33520
Society 	33305, 33471, 37212, or 38119	30133, 33251 (along with enrollment in 33250),34113, 34117, 38115, 38126, 42201
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
    2. Lists specific course numbers that satisfy the requirements
    3. Do not make up course names, only list course numbers

    Response:"""
)

@tool
def degree_requirements_checker(text: str):
    """
    A tool for students at the Booth School of Business to determine what courses they need to take to fulfill their degree requirements.
    """
    try:
        # Generate the prompt with the student's query
        prompt = COURSE_PLANNER_PROMPT.format(
            degree_requirements=DEGREE_REQUIREMENTS,
            query=text
        )
        
        # Get response from the LLM
        response = llm.invoke(prompt)
        return response.content
            
    except Exception as e:
        return f"Error in course planning: {str(e)}"

# Example usage
if __name__ == "__main__":

    print(degree_requirements_checker("What courses can I take to fulfill the Finance requirement?"))

    exit()
    # Example queries to test the tool
    test_queries = [
        "What courses can I take to fulfill the Financial Accounting requirement?",
        "I need to take Microeconomics next quarter. What are my options?",
        "Which Statistics courses are available for the MBA program?"
    ]
    
    # Test the tool with each query
    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {degree_requirements_checker(query)}")