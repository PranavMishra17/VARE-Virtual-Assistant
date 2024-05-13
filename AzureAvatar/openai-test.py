import os
import time
import json
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

# Create an assistant
assistant = client.beta.assistants.create(
    name="VARE Lab Assistant",
    instructions="You are an AI lab assistant.",
    tools=[],
    model="assistantPreviewSaturday" #You must replace this value with the deployment name for your model.  # assistantPreviewSaturday
)

# Create a thread
thread = client.beta.threads.create()

# Add a user question to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hi, what projects are you working on?"
)

# Run the thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

# Retrieve the status of the run
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

status = run.status

# Wait till the assistant has responded
while status not in ["completed", "cancelled", "expired", "failed"]:
    time.sleep(5)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    status = run.status

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.model_dump_json(indent=2))

# Directly print the messages to see what's included
for message in messages:
    print(f"ID: {message.id}, Content: {message.content}, Role: {message.role}")
