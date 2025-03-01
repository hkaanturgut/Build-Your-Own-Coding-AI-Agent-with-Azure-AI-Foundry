import json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Replace these with your actual values
PROJECT_CONNECTION_STRING = ""
AGENT_ID = ""  # Replace with actual agent ID from setup_agent.py

def chat_with_agent(agent_id):
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(), conn_str=PROJECT_CONNECTION_STRING
    )

    with project_client:
        # Create a chat thread
        thread = project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")

        # Send a message
        message = project_client.agents.create_message(
            thread_id=thread.id, role="user", content="What is our Python coding standard?"
        )
        print(f"Created message, message ID: {message.id}")

        # Process the request
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_id)
        print(f"Created run, run ID: {run.id}")

        # Fetch responses
        messages = project_client.agents.list_messages(thread_id=thread.id)

        # Extract assistant's response
        for message in messages["data"]:
            if message["role"] == "assistant":
                response_content = message["content"][0]["text"]["value"]
                response_json = {
                    "message_id": message["id"],
                    "created_at": message["created_at"],
                    "assistant_id": message["assistant_id"],
                    "thread_id": message["thread_id"],
                    "response": response_content
                }
                print(json.dumps(response_json, indent=4))

if __name__ == "__main__":
    chat_with_agent(AGENT_ID)
