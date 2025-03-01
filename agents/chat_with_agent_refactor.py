import os
import json
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FilePurpose, MessageAttachment, FileSearchTool
from azure.identity import DefaultAzureCredential

# Replace these with your actual values
PROJECT_CONNECTION_STRING = ""
AGENT_ID = ""  # Replace with actual agent ID from setup_agent.py
VECTOR_STORE_ID = ""  # Replace with actual Vector Store ID from setup_agent.py
SCRIPT_FILE_PATH = "broken-scripts/py-nonstandard-script.py"  # Path to script for refactoring
OUTPUT_FILE_PATH = "refactored_scripts/refactored_script.py"  # Path to save the refactored script


def chat_with_agent_refactor(agent_id, script_path, output_file, vector_store_id):
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"The script file {script_path} does not exist.")

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(), conn_str=PROJECT_CONNECTION_STRING
    )

    with project_client:
        # Create a new chat thread
        thread = project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")

        # Upload the script file
        script_file = project_client.agents.upload_file_and_poll(file_path=script_path, purpose=FilePurpose.AGENTS)
        print(f"Uploaded script file, file ID: {script_file.id}")

        # ✅ Use the same vector store created in `setup_agent.py`
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store_id])

        # Create a message with the script file attachment
        attachment = MessageAttachment(file_id=script_file.id, tools=file_search_tool.definitions)

        # ✅ Explicitly instruct the agent to use the coding standards from the vector store
        message_content = (
            f"I have attached a Python script (`{os.path.basename(script_path)}`). "
            "Please refactor this script according to our company coding standards. "
            "Use the Python coding standards stored in the knowledge base (File Search Tool). "
            "Make sure to fix any non-standard practices and improve readability."
        )

        message = project_client.agents.create_message(
            thread_id=thread.id, role="user", content=message_content, attachments=[attachment]
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

                # Print a readable response
                print("\n✅ AI Refactored Script:")
                print("-" * 50)
                print(response_content)
                print("-" * 50)

                # Extract only the Python code from the response
                if "```python" in response_content and "```" in response_content:
                    refactored_code = response_content.split("```python")[1].split("```")[0].strip()
                else:
                    refactored_code = response_content

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                # Save the refactored script to a file
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(refactored_code)

                print(f"\n🚀 Refactored script saved to: {output_file}\n")


if __name__ == "__main__":
    chat_with_agent_refactor(AGENT_ID, SCRIPT_FILE_PATH, OUTPUT_FILE_PATH, VECTOR_STORE_ID)