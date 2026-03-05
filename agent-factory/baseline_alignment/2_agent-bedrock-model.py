from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-3-haiku-20240307-v1:0",  
    temperature=0.3,                          
    top_p=0.8,
    streaming=True
)

agent = Agent(model=model)
response = agent("What is AWS re:Invent? Answer in one sentence.")