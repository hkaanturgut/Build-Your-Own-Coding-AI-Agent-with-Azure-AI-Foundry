import os
import json
import requests
import logging
from requests.auth import HTTPBasicAuth
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageAttachment, FileSearchTool, FilePurpose
from azure.identity import DefaultAzureCredential
from datetime import datetime

# ✅ Azure DevOps Configuration
ADO_ORG = ""  # Azure DevOps Organization
ADO_PROJECT = ""  # Azure DevOps Project
ADO_REPO = ""  # Azure DevOps Repository
ADO_PAT = os.getenv("ADO_PAT")  # Azure DevOps Personal Access Token (set as environment variable)
ADO_BASE_URL = f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_apis"
WORK_ITEM_ID = ""  # Work Item ID
BRANCH_NAME = f"feature/workitem-{WORK_ITEM_ID}"  # Create a feature branch per task
TARGET_BRANCH = "main"  # Target branch for the pull request

# ✅ Azure AI Foundry Configuration
PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")  # Project connection string (set as environment variable)
AGENT_ID = os.getenv("AGENT_ID")  # AI Agent ID (set as environment variable)
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")  # Vector Store ID (set as environment variable)
Language = "Java"

# ✅ File Paths

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
GENERATED_SCRIPT_PATH = f"generated_scripts/script_{WORK_ITEM_ID}_{timestamp}.java"

# ✅ Function to Fetch Work Item Details
def get_work_item(work_item_id):
    if not ADO_PAT:
        raise Exception("❌ Error: Azure DevOps PAT is missing. Set the ADO_PAT environment variable!")

    url = f"{ADO_BASE_URL}/wit/workitems/{work_item_id}?api-version=6.0"
    response = requests.get(url, auth=HTTPBasicAuth("", ADO_PAT))

    if response.status_code == 200:
        work_item = response.json()
        title = work_item["fields"].get("System.Title", "No Title")
        description = work_item["fields"].get("System.Description", "No Description")
        print(f"✅ Retrieved Work Item: {title}\n")

        work_item_text = f"Task: {title}\nDescription: {description}"
        print(f"📌 Work Item Details:\n{work_item_text}\n")

        return work_item_text  # 🔥 Pass this to AI Agent

    elif response.status_code == 401:
        raise Exception("❌ Authentication failed! Check your Azure DevOps PAT permissions.")

    else:
        raise Exception(f"❌ Failed to fetch work item. Status: {response.status_code}, Response: {response.text}")

# ✅ Function to Generate a Script using AI Foundry Agent
def generate_script(agent_id, output_file, work_item_details):
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(), conn_str=PROJECT_CONNECTION_STRING
    )

    with project_client:
        # Create a new chat thread
        thread = project_client.agents.create_thread()
        print(f"📌 Created thread, ID: {thread.id}")

        # ✅ Ask AI to generate a script based on the work item
        message_content = (
            "Please generate a {Language} script based on the following task requirements:\n\n"
            f"{work_item_details}\n\n"
            "Ensure that the script follows the company standards and best practices, is well-documented with comments, "
            "and includes error handling."
        )

        message = project_client.agents.create_message(
            thread_id=thread.id, role="user", content=message_content
        )
        print(f"📩 Sent task to AI agent, message ID: {message.id}")

        # Process the request
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent_id)
        print(f"🔄 Processing AI request, ID: {run.id}")

        # Fetch responses
        messages = project_client.agents.list_messages(thread_id=thread.id)

        # Extract AI-generated script
        for message in messages["data"]:
            if message["role"] == "assistant":
                response_content = message["content"][0]["text"]["value"]

                # Extract Python script from response
                if "```python" in response_content:
                    script_code = response_content.split("```python")[1].split("```")[0].strip()
                else:
                    script_code = response_content

                # Save the script to a file
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(script_code)

                print(f"\n✅ New script generated and saved at: {output_file}\n")
                return script_code

    return None

# ✅ Function to Fetch the Latest Commit ID from Main Branch
def get_latest_commit():
    url = f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_apis/git/repositories/{ADO_REPO}/commits?searchCriteria.itemVersion.version={TARGET_BRANCH}&api-version=7.1"
    
    response = requests.get(url, auth=HTTPBasicAuth("", ADO_PAT))

    if response.status_code == 200:
        commit_data = response.json()

        # ✅ Handle missing or empty branches
        if "value" in commit_data and len(commit_data["value"]) > 0:
            latest_commit_id = commit_data["value"][0]["commitId"]
            logging.info(f"✅ Latest commit ID of {TARGET_BRANCH}: {latest_commit_id}")
            return latest_commit_id
        else:
            logging.error(f"❌ No commits found in branch '{TARGET_BRANCH}'. Please check if the branch exists and has at least one commit.")
            raise Exception(f"No commits found in branch '{TARGET_BRANCH}'.")

    else:
        logging.error(f"❌ Failed to fetch latest commit ID. Response: {response.text}")
        raise Exception(f"Failed to fetch latest commit ID. Status Code: {response.status_code}")

# ✅ Function to Create a New Branch from Main
def create_branch():
    latest_commit_id = get_latest_commit()  # ✅ Get the latest commit ID from main

    url = f"{ADO_BASE_URL}/git/repositories/{ADO_REPO}/refs?api-version=7.1"

    branch_payload = [
        {
            "name": f"refs/heads/{BRANCH_NAME}",
            "oldObjectId": "0000000000000000000000000000000000000000",  # New branch
            "newObjectId": latest_commit_id,  # ✅ Dynamically use the latest commit ID
        }
    ]

    response = requests.post(url, auth=HTTPBasicAuth("", ADO_PAT), json=branch_payload)

    if response.status_code in [200, 201]:
        logging.info(f"✅ Created new branch: {BRANCH_NAME}")
        return True
    else:
        logging.error(f"❌ Branch creation failed. Response: {response.text}")
        return False


# ✅ Run the Script
if __name__ == "__main__":
    logging.info("\n🚀 Starting Branch Creation Process...\n")
    
    if create_branch():
        logging.info("\n✅ Branch Creation Completed Successfully!\n")
    else:
        logging.error("\n❌ Branch Creation Failed.\n")

# ✅ Function to Check If a File Exists in the Repo
def check_file_exists(file_path):
    url = f"{ADO_BASE_URL}/git/repositories/{ADO_REPO}/items?path={file_path}&api-version=7.1"
    response = requests.get(url, auth=HTTPBasicAuth("", ADO_PAT))

    if response.status_code == 200:
        logging.info(f"📂 File {file_path} exists in the repository. Updating it...")
        return True  # File exists, so we must use "edit"
    elif response.status_code == 404:
        logging.info(f"🆕 File {file_path} does not exist in the repository. Adding it...")
        return False  # File doesn't exist, so we must use "add"
    else:
        logging.error(f"❌ Failed to check file existence. Response: {response.text}")
        raise Exception("Failed to check file existence in repo.")

# ✅ Function to Commit and Push Script to Azure DevOps
def commit_script():
    latest_commit_id = get_latest_commit()  # Get latest commit ID

    url = f"{ADO_BASE_URL}/git/repositories/{ADO_REPO}/pushes?api-version=7.1"

    with open(GENERATED_SCRIPT_PATH, "r") as f:
        script_content = f.read()

    file_exists = check_file_exists(f"/{GENERATED_SCRIPT_PATH}")  # Check if the file already exists

    commit_payload = {
        "refUpdates": [
            {
                "name": f"refs/heads/{BRANCH_NAME}",
                "oldObjectId": latest_commit_id,
            }
        ],
        "commits": [
            {
                "comment": f"Generated script for Work Item {WORK_ITEM_ID} via AI Agent",
                "changes": [
                    {
                        "changeType": "edit" if file_exists else "add",  # ✅ Use "edit" if the file exists
                        "item": {"path": f"/{GENERATED_SCRIPT_PATH}"},
                        "newContent": {"content": script_content, "contentType": "rawtext"},
                    }
                ],
            }
        ],
    }

    response = requests.post(url, auth=HTTPBasicAuth("", ADO_PAT), json=commit_payload)

    if response.status_code == 201:
        logging.info(f"✅ Script committed successfully to branch: {BRANCH_NAME}")
        return True
    else:
        logging.error(f"❌ Commit failed. Response: {response.text}")
        return False


# ✅ Function to Create a Pull Request in Azure DevOps
def create_pull_request():
    url = f"{ADO_BASE_URL}/git/repositories/{ADO_REPO}/pullrequests?api-version=6.0"

    pr_payload = {
        "sourceRefName": f"refs/heads/{BRANCH_NAME}",
        "targetRefName": f"refs/heads/{TARGET_BRANCH}",
        "title": f"AI Generated Script for Work Item {WORK_ITEM_ID}",
        "description": "This pull request was automatically generated by the AI Agent.",
    }

    response = requests.post(url, auth=HTTPBasicAuth("", ADO_PAT), json=pr_payload)

    if response.status_code == 201:
        pr_data = response.json()
        pr_url = pr_data["url"]
        print(f"✅ Pull request created: {pr_url}")
    else:
        print(f"❌ PR creation failed. Response: {response.text}")

# ✅ Run the script
if __name__ == "__main__":
    print("\n🚀 Starting Work Item Processing...\n")

    # Step 1: Fetch Work Item
    work_item_details = get_work_item(WORK_ITEM_ID)

    # Step 2: Generate the script using AI Agent
    print("\n🛠️ Generating Script Based on Work Item Details...\n")
    generated_code = generate_script(AGENT_ID, GENERATED_SCRIPT_PATH, work_item_details)

    if generated_code:
        print("\n✅ Script Generation Completed Successfully!\n")

        # Step 3: Create Branch in Azure DevOps
        if create_branch():
            # Step 4: Commit and Push the Script
            if commit_script():
                # Step 5: Create Pull Request
                create_pull_request()
            else:
                print("\n❌ Commit failed. Skipping PR creation.\n")
        else:
            print("\n❌ Branch creation failed. Skipping commit & PR.\n")
    else:
        print("\n❌ Script Generation Failed.\n")