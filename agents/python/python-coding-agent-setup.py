import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FilePurpose, FileSearchTool
from azure.identity import DefaultAzureCredential

# Replace these with your actual values
PROJECT_CONNECTION_STRING = ""
MODEL_DEPLOYMENT_NAME = ""
name = "python-coding-agent"
standards_file_path = "instructions/py-standard-instructions.py"
vector_store_name = "Python-Coding-Standards-Vector-Store"

def setup_agent():
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(), conn_str=PROJECT_CONNECTION_STRING
    )

    with project_client:
        # Upload the standard instructions file
        standards_file = project_client.agents.upload_file_and_poll(
            file_path=standards_file_path, purpose=FilePurpose.AGENTS
        )
        print(f"Uploaded standards file, file ID: {standards_file.id}")

        # Create a vector store
        vector_store = project_client.agents.create_vector_store_and_poll(
            file_ids=[standards_file.id], name=vector_store_name
        )
        print(f"Created vector store, vector store ID: {vector_store.id}")

        # Create a file search tool
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

        # Load agent instructions
        instructions_file_path = "agents/python/agent-instructions.text"
        if not os.path.exists(instructions_file_path):
            raise FileNotFoundError(f"The file {instructions_file_path} does not exist.")
        
        with open(instructions_file_path, "r") as file:
            instructions = file.read()

        # Create agent
        agent = project_client.agents.create_agent(
            model=MODEL_DEPLOYMENT_NAME,
            name=name,
            instructions=instructions,
            tools=file_search_tool.definitions,
            tool_resources=file_search_tool.resources,
        )
        print(f"Created agent, agent ID: {agent.id}")

        return agent.id, vector_store.id

if __name__ == "__main__":
    agent_id, vector_store_id = setup_agent()
    print(f"Setup complete. Agent ID: {agent_id}, Vector Store ID: {vector_store_id}")
