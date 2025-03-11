<div align="center">
  <img src="frontend/assets/chicago-booth_logo.jpg" alt="Chicago Booth Logo" width="600"/>
</div>

# Booth Course Assistant Chatbot

A comprehensive chatbot designed to help Booth School of Business students with course-related queries, including course information, bidding history, and degree requirements.

## Features

The chatbot provides assistance with:
- Course information and prerequisites
- Degree requirements
- Concentration requirements
- Course bidding history and analysis
- Course syllabi information
- Real-time course scheduling information

## Backend Architecture

### Core Components
- **Framework**: Flask-based REST API
- **AI Model**: GPT-4 powered by LangChain
- **Memory**: Conversation buffer for context retention
- **Thinking Process**: Transparent reasoning with step-by-step thought process

### Tools and Integrations
1. **Course Information Tools**
   - Vector-based course search
   - Context-based course search
   - Course number to title mapping

2. **Academic Requirements**
   - Degree requirements checker
   - Concentration requirements validator

3. **Bidding Analysis**
   - Historical bidding data processor
   - Bid point analysis and recommendations

4. **Data Processing**
   - Excel to CSV conversion for bidding data
   - Course data vectorization
   - Syllabus parsing and analysis

## Frontend Interface

### Technologies
- **Framework**: Streamlit
- **Features**:
  - Clean, intuitive chat interface
  - Real-time response display
  - Expandable thinking process view
  - Chat history management
  - Raw response data access
  - Error handling with user feedback

### User Interface Components
- Query input field
- Chat history display
- Thinking process expansion
- Response formatting
- Error notifications
- Clear chat functionality

## Setup and Installation

### Prerequisites
```bash
# Required Python version
Python 3.12 (Tested and recommended)

# Required environment variables
OPENAI_API_KEY=your_api_key_here
```

### Installation Steps

1. Clone the repository:
```bash
git clone git@github.com:bilalbaqar/booth-chatbot.git

# If you dont want to use ssh to clone
# git clone https://github.com/bilalbaqar/booth-chatbot.git

cd booth-chatbot
```

2. Set up Python environment (choose one option):

#### Option A: Using Conda (Recommended)
```bash
# Create and activate conda environment
conda create --name env-booth-chatbot python=3.12
conda activate env-booth-chatbot

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using venv
```bash
# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
touch .env  # On Windows: type nul > .env

# Add the following content to your .env file:
OPENAI_API_KEY=your_api_key_here

# You can do this via command line:
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Or manually create/edit the .env file in your preferred text editor
# and add the following line:
# OPENAI_API_KEY=your_api_key_here
```

Note: Replace `your_api_key_here` with your actual OpenAI API key. You can get an API key from [OpenAI's website](https://platform.openai.com/api-keys).

### Running the Application

1. Start the backend server:
```bash
python .\booth_agent\booth-agent.py --server --server
```

2. Start the frontend interface (in a new terminal):
```bash
streamlit run frontend\chatbot-frontend.py
```

The application will be available at:
- Frontend: http://localhost:8501
- Backend API: http://localhost:5000

### Alternative Run Modes

The backend supports different modes of operation:

```bash
# Run in CLI mode for command-line interaction
python booth-agent.py --cli

# Run test queries
python booth-agent.py --test

# Show help
python booth-agent.py --help
```

## Tools and Dependencies

### Main Libraries
- `langchain`: For AI model integration and chain management
- `openai`: For GPT-4 API access
- `flask`: For backend API server
- `streamlit`: For frontend interface
- `pandas`: For data processing
- `numpy`: For numerical operations
- `requests`: For API communication

### Data Processing Tools
- `DocArrayInMemorySearch`: For vector search capabilities
- `CSVLoader`: For data loading and processing
- `OpenAIEmbeddings`: For text embeddings