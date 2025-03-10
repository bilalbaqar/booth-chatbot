from langchain.prompts import PromptTemplate

REACT_PROMPT = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Important: 
    1. Always start with "Question: " followed by the input
    2. Each Thought/Action/Action Input/Observation must be on a new line
    3. The Final Answer must be on a new line starting with "Final Answer: "
    4. Do not combine multiple actions in one step
    5. Make sure to include all required fields in the correct order

    Additional Instructions:
    - If course numbers are found in the response, run the **course_to_title** tool for each course number.
    - When responding with the final answer, include both the course title and its corresponding course number.


    Begin!

    Question: {input}
    Thought: {agent_scratchpad}"""
) 
