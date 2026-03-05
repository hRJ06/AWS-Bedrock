from strands import Agent
from strands_tools import editor
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    streaming=True
)

agent = Agent(
    model=model,
    system_prompt="""
    Goal:
    - Create a python tool under cwd()/tools/*.py using given python tool decorator.
    - I have hot-reloading abilities, after writing the file, I can use it immediately.

    Building tools:
    

    from strands import tool

    @tool
    def name(name: str, description: str) -> str:
        '''
        Create a tool under cwd()/tools/*.py.
        '''
        return ""
        
    """,
    tools=[editor],
    load_tools_from_directory=True
)

response = agent("Create a tool to add two numbers and use the tool to add 5 and 7.")