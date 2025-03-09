from langchain_core.tools import tool
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from IPython.display import display, Markdown
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.indexes import VectorstoreIndexCreator

from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()


llm_model = "gpt-4o-mini"


file = os.path.abspath(r'..\data\all-course-list.csv')

loader = CSVLoader(file_path=file)

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=OpenAIEmbeddings()
).from_loaders([loader])

query ="What is the course number for investments?"


llm_replacement_model = OpenAI(temperature=0, 
                               model='gpt-3.5-turbo-instruct')









response = index.query(query, 
                       llm = llm_replacement_model)

display(Markdown(response))






# Initialize the language model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini"
)

# Create the prompt template
COURSE_PLANNER_PROMPT = PromptTemplate.from_template(
    """You are a course planning assistant for the Booth School of Business MBA program. 
    Use the following degree requirements to help students plan their courses:

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
def course_info(text: str):
    """
    A tool for students at the Booth School of Business to determine what courses are offered in different quarters.
    This tool also allows students to search for courses by name and provides them with the course number.
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