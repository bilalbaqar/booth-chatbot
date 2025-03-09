from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini"
)

class CSVQuestionAnswerer:
    def __init__(self, csv_file_path: str):
        """
        Initialize the CSV Question Answerer.
        
        Args:
            csv_file_path (str): Path to the CSV file to load.
        """
        self.csv_file_path = csv_file_path
        self.documents = self._load_csv()
        self.context = self._create_context()

        # Define a prompt template for structured responses
        self.prompt = PromptTemplate(
            template="""You are an assistant that answers questions about data from a CSV file.
            
            Here is the CSV data:
            {context}
            
            Please answer the following question based only on the given data.
            
            Question: {question}
            
            If the answer cannot be determined from the data, clearly state that.
            
            Answer:""",
            input_variables=["context", "question"]
        )

    def _load_csv(self):
        """
        Load the CSV file and return its content.
        """
        try:
            loader = CSVLoader(
                file_path=self.csv_file_path,
                encoding="utf-8",
                csv_args={'delimiter': ',', 'quotechar': '"'}
            )
            return loader.load()
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")

    def _create_context(self) -> str:
        """
        Create a string representation of the CSV data.
        """
        return "\n".join(doc.page_content for doc in self.documents)

    def ask(self, question: str) -> str:
        """
        Ask a question based on the CSV data.
        
        Args:
            question (str): The question to ask.
            
        Returns:
            str: The answer to the question.
        """
        try:
            response = llm.invoke(self.prompt.format(
                context=self.context,
                question=question
            ))
            return response.content
        except Exception as e:
            return f"Error processing question: {str(e)}"

# Define as a LangChain tool
@tool
def csv_question_answerer(question: str):
    """
    A tool for querying structured CSV data using a language model.
    
    Example:
    - "What is the course number for investments?"
    - "What courses are available in Spring 2025?"
    """
    try:
        # Path to CSV file
        csv_file = os.path.abspath(r'..\data\all-course-list.csv')
        qa = CSVQuestionAnswerer(csv_file)
        return qa.ask(question)
    except Exception as e:
        return f"Error processing request: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Example test cases
    test_queries = [
        "What is the total number of records in the dataset?",
        "What are the column names in the dataset?",
        "What is the course number for investments?",
        "What are the course numbers for investments and financial accounting?",
        "What courses are offered in Spring 2025?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {csv_question_answerer(query)}")
