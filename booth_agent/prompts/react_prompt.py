from langchain.prompts import PromptTemplate

REACT_PROMPT = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Previous conversation history:
    {chat_history}

    Current question: {input}

    Use the following format:

    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Important: 
    1. Each Thought/Action/Action Input/Observation must be on a new line
    2. The Final Answer must be on a new line starting with "Final Answer: "
    3. Do not combine multiple actions in one step
    4. Make sure to include all required fields in the correct order
    5. Use the chat history to understand context and previous information

    Additional Instructions:
    - If query is a phrase like "hello" or "hi", just respond with a greeting as Final Answer. 
    - If course numbers are found in the response, run the **course_to_title** tool for each course number
    - When responding with the final answer, try to include both the course title and its corresponding course number
    - If **course_to_title** does not return a course title then just return the course number
    - Use the conversation history to provide more context-aware responses and avoid repeating information
    - If a course number was mentioned in previous messages, use that information

    Begin!

    Thought: {agent_scratchpad}"""
) 
