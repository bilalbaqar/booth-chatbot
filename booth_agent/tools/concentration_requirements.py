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

# Define the concentration requirements
CONCENTRATION_REQUIREMENTS = """
Chicago Booth students may pursue the concentration offerings listed below. A notation is made on their official transcript if a concentration is completed. Concentrations are not required for graduation.

For more information, please see the Chicago Booth Student Handbook. For course details, consult the full course descriptions.

*Revised December 18, 2024

Accounting
400 credit units chosen from the following list: Business 30000, 30005 (or 30001), 30116, 30118, 30120, 30121, 30122, 30130, 30131, 30132, 30133, 30135, 30830, 30835, 30840.

Behavioral Science
400 credit units chosen from the following list: Business 31403, 31702, 38001, 38002, 38003, 38101, 38102, 38103, 38105, 38107, 38115, 38116, 38118, 38119, 38120, 38122, 38123, 38126, 38820, 38821, 38825, 38870, 38865, 38875, 38886, and 39002.

Business Analytics
100 credit units in data science: Business 41201 or 41204.
100 credit units in decision models and optimization: Business 36106 or 36109.
An additional 300 units of elective credit from: Business 30135, 32100, 32105, 32120, 32130, 32200, 32210, 32810, 33222, 36109, 37103, 37105, 37107, 37202, 37802, 40108, 40206 (or 40205), 40721, 41201, 41202, 41203, 41204, 41301 (or 41305), and 41814. No more than 200 units of elective credit from each area will be counted.

Business, Society and Sustainability
400 credit units from the following list:
- Social Sector Institutions: Business 34113, 34115, 34117, 42125, 42710, or 42711.
- Corporate Citizenship, Purpose, & ESG: Business 30133, 31425, 37212, 38112, or 42708.
- Role of Business in Society: Business 33305, 33251 (with 33250), 35225, or 42129.
- Ethics: Business 38119, 33471, 38115, 38128.

Econometrics and Statistics
300 credit units chosen from: Business 41000, 41100, 41201, 41202, 41203, 41204, 41206 (or 41813), 41207, 41301 (or 41305), 41813, 41814, 41901, 41902, 41903, and 41910.

Economics
400 credit units chosen from: Business 33032, 33050 (or 33040), 33101, 33112, 33222, 33230, 33251 (with 33250), 33301, 33305, 33350, 33401, 33403, 33454, 33501 (or 33502 or 33503), 33520, 33882, 38120, 42001, 42116, and 42135. Business 33001 and 33002 do not qualify.

Entrepreneurship
300 credit units chosen from: Business 30118, 30121, 31401, 31402, 31403, 34101, 34102, 34103, 34104, 34106, 34108, 34111, 34113, 34115, 34117, 34205, 34206, 34208, 34210, 34211, 34219, 34220, 34302, 34305, 34306, 34702, 34704, 34705, 34709, 34715, 34815, 34816, 34820, 34825, 34826, 34880, 34887, 34888, 35123, 35213, 35823, 36110, 36820, 37200, 37201, 37301, 37703, 39101, 40110, 41206 (or 41813), 41301 (or 41305), 41813, 42705, 42711, 42820, and LAWS 43225.

Note: Students cannot take both 37200 and 37201. Students who took 34702 are not eligible to take 34707 or 34708. Students can count only 100 units of credit toward both the entrepreneurship and strategic management concentrations.

Finance
100 units in asset pricing: Business 34901, 34902, 35000, 35100, 35101, 35120, 35121, 35126, 35130, 35131, 35132, 35901, 35908.
100 units in corporate finance: Business 34101, 34903, 34904, 35200, 35201, 35202, 35210, 35213, 35214, and 35215.
An additional 200 units from: Business 30130, 30131, 34101, 34901, 34902, 34903, 34904, 35100, 35101, 35120, 35121, 35123, 35124, 35126, 35130, 35131, 35132, 35133, 35136 (or 35135), 35137, 35145, 35150, 35201, 35202, 35207, 35210, 35213, 35214, 35215, 35219, 35222 (or 35220), 35225 (ECON 28620), 35823, 35824, 35881, 35889, 35901, 35907, 35908, and 41203.

Note: Courses meeting a finance concentration, but not an analytic finance concentration, include Business 30130, 30131, 35000, 35101, and 35123.

Analytic Finance
600 credit units chosen from: Business 34101, 34901, 34902, 34903, 34904, 35100, 35120, 35121, 35126, 35130, 35131, 35132, 35133, 35150, 35200, 35201, 35202, 35210, 35213, 35214, 35215, 35219, 35901, 35907, 35908, and 41203. The student must also satisfy the finance requirements.

General Management
To complete the general management concentration, students must complete all eight lines (800 credit units) of the Functions, Leadership and Management, and the Business Environment requirements, plus an additional 300 credit units from courses in strategic management, behavioral science, or a combination of both for a total of 1100 credit units.

Healthcare
400 credit units. At least 100 core credit units from 33350, 40206 (or 40205). 200-300 credit units from: 33351, 33352, 34205, 34210, 42300, or 42310. Up to 100 credit units of a pre-approved experiential healthcare course from: 34104, 34115, 34702, 34705, 34709, 37201, 37703, 40721, 42709, 42710.

International Business
300 credit units chosen from: Business 30131, 33501, 33502, 33503, 33520, 35210, 35213, and 35219. At least one must be 33501 or 33502.

Marketing Management
Business 37000 (or 37110) and at least 300 credit units from: Business 37101, 37103 (or 37105), 37107, 37110, 37200, 37201, 37202, 37208, 37209, 37212, 37301, 37703, 37810, 37816, 37882, 37902, and 41301 (or 41305).

Operations Management
300 credit units chosen from: Business 36106, 36109, 40000, 40101, 40108, 40110, 40111, 40206 (or 40205), 40721, 40810, and 40811.
"""

# Create the prompt template
CONCENTRATION_PROMPT = PromptTemplate.from_template(
    """You are a concentration requirements assistant for the Booth School of Business MBA program.
    Use the following concentration requirements to help students determine if a course fulfills their requirements:

    {concentration_requirements}

    When answering:
    1. Directly answer the student's query.
    2. List course numbers that fulfill the requirements.
    3. Ensure accuracy—do not fabricate courses.
    
    Student's question: {query}

    Response:"""
)

@tool
def concentration_requirements_checker(text: str):
    """
    A tool for students at the Booth School of Business to determine what courses fulfill concentration requirements.
    """
    try:
        # Generate the prompt with the student's query
        prompt = CONCENTRATION_PROMPT.format(
            concentration_requirements=CONCENTRATION_REQUIREMENTS,
            query=text
        )
        
        # Get response from the LLM
        response = llm.invoke(prompt)
        return response.content
            
    except Exception as e:
        return f"Error in checking concentration requirements: {str(e)}"

# Example usage
if __name__ == "__main__":
    
    print(concentration_requirements_checker("What courses fulfill requirements for Accounting concentration?"))
    
    # Example queries to test the tool
    test_queries = [
        "Does 30131 fulfill requirements for Accounting concentration?",
        "Which courses fulfill the requirements for both Entrepreneurship and Finance?",
        "Can I count 41201 towards Business Analytics and Finance?",
        "What courses fulfill requirements for Accounting concentration?",
        "Does 30131 fulfill requirements for Accounting concentration?",
        "Which courses fulfill the requirements for both Entrepreneurship and General Management"
    ]
    
    # Test the tool with each query
    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {concentration_requirements_checker(query)}")