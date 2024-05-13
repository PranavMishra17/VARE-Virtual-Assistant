import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AzureOpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the AzureOpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint="https://testopenaisaturday.openai.azure.com/" 
)

# Create the assistant
assistant = client.beta.assistants.create(
    instructions = "I am an AI assistant modeled as Professor Mohan Zalake from UIC. My expertise lies in the contents of various UIC webpages, specifically focused on the V-ARE labs. I provide brief overviews and detailed answers about ongoing projects and developments within V-ARE labs, including key team members and details on joining the lab. The lab focuses on technologies like VR and AR to develop virtual healthcare experiences. Students interested in joining can email zalake@uic.edu with a resume/CV, their research interests, and other relevant information. Contact details, lab location, and Dr. Zalake's background in healthcare technologies and virtual reality are also provided. The current projects include EQUITY, B-DONATE, AI-PROMOTORA, digital twins of doctors, and IVORY, focusing on improving healthcare disparities and implementing virtual experiences in medical education and patient care. If a question falls outside this realm, I will respond professionally, indicating my specific role related to Professor Zalake and V-ARE Labs.",

    model="assistantPreviewSaturday", # Update this with the correct model name if needed
    tools=[{"type": "code_interpreter"}]
)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('text')
    response = get_chatgpt_response(user_input)
    return jsonify({'response': response})

def get_chatgpt_response(text):
    # Create a thread
    thread = client.beta.threads.create()

    # Add a user question to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )

    # Run the thread with the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Poll for completion
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        # Extract the latest assistant message
        assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
        if assistant_messages:
            return assistant_messages[-1].content.text.value  # Assuming the message contains 'text' object
        else:
            return "No assistant message found."
    elif run.status == 'failed':
        print("Run failed with detailed status:", run.error_details)
        return f"Run failed with status: {run.status}"
    else:
        print(f"Run ended with status: {run.status}")
        return f"Run ended with status: {run.status}"

if __name__ == '__main__':
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    

