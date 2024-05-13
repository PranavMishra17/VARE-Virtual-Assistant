import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AzureOpenAI

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

inst = "I am an AI assistant modeled as Professor Mohan Zalake from UIC. My expertise lies in the contents of various UIC webpages, specifically focused on the V-ARE labs. I provide brief overviews and detailed answers about ongoing projects and developments within V-ARE labs, including key team members and details on joining the lab. The lab focuses on technologies like VR and AR to develop virtual healthcare experiences. Students interested in joining can email zalake@uic.edu with a resume/CV, their research interests, and other relevant information. Contact details, lab location, and Dr. Zalake's background in healthcare technologies and virtual reality are also provided. The current projects include EQUITY, B-DONATE, AI-PROMOTORA, digital twins of doctors, and IVORY, focusing on improving healthcare disparities and implementing virtual experiences in medical education and patient care. If a question falls outside this realm, I will respond professionally, indicating my specific role related to Professor Zalake and V-ARE Labs."

# Initialize the AzureOpenAI client with environment variables
azure_endpoint = "https://testopenaisaturday.openai.azure.com/" 
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = "2024-02-15-preview"
client = AzureOpenAI(azure_endpoint=azure_endpoint, api_key=api_key, api_version=api_version)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('text')
    response = get_chatgpt_response(user_input)
    return jsonify({'response': response})

def get_chatgpt_response(text):
    message_text = [
        {"role": "system", "content": inst},
        {"role": "user", "content": text}
    ]

    try:
        # Create a chat completion request with the specified model and parameters
        completion = client.chat.completions.create(
            model="assistantPreviewSaturday",
            messages=message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        # Convert the completion object to a string for manual parsing
        completion_str = str(completion)
        #print("Complete API response as string:", completion_str)

        # Manual parsing to find the content after 'message=ChatCompletionMessage(content='
        start_marker = "message=ChatCompletionMessage(content='"
        end_marker = "', role='assistant'"

        start_pos = completion_str.find(start_marker)
        if start_pos != -1:
            start_pos += len(start_marker)
            end_pos = completion_str.find(end_marker, start_pos)
            if end_pos != -1:
                # Extract the message content
                message_content = completion_str[start_pos:end_pos]
                return message_content
            else:
                return "End marker not found."
        else:
            return "Start marker not found."

    except Exception as e:
        print(f"Error making API call: {e}")
        return f"Error: {str(e)}"




if __name__ == '__main__':
    app.run(port=5000, debug=True)
