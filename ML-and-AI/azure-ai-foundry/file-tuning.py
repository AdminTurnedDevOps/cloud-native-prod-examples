from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, MessageAttachment, FilePurpose

fileLocation = '/Users/michael/Downloads/keda.pdf'
question = "Tell me how to programmatically create a KEDA Cron Job for a Pod"

def main():
    fileSearch()

def project():
    project_connection_string="eastus.api.azureml.ms;;rg-michaanai;pythonTesting"

    project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string,
    credential=DefaultAzureCredential())
    
    return project

def upload():
    #upload file
    file = project().agents.upload_file_and_poll(file_path=fileLocation, purpose=FilePurpose.AGENTS)

    # create a vector store with the file you uploaded
    vector_store = project().agents.create_vector_store_and_poll(file_ids=[file.id], name="kedaSearch")
    
    return vector_store

def fileSearch():
    # create a file search tool
    file_search_tool = FileSearchTool(vector_store_ids=[upload().id])

    # notices that FileSearchTool as tool and tool_resources must be added or the agent will be unable to search the file
    agent = project().agents.create_agent(
        model="DeepSeek-R1",
        name="KEDA",
        instructions="You help me with Kubernetes Event-Drive Autoscaling",
        tools=file_search_tool.definitions,
        tool_resources=file_search_tool.resources,
        )
    
    thread = project().agents.create_thread()
    thread.id
    
    message_file = project().agents.upload_file_and_poll(file_path=fileLocation, purpose=FilePurpose.AGENTS)
    message_file.id
    
    attachment = MessageAttachment(file_id=message_file.id, tools=FileSearchTool().definitions)
    
    message = project().agents.create_message(
    thread_id=thread.id, role="user", content=question, attachments=[attachment]
    )
    
    print(message.id)
    
    # run = project().agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    # print(f"Created run, run ID: {run.id}")

    # project().agents.delete_vector_store(vector_store.id)
    # print("Deleted vector store")

    # project_client.agents.delete_agent(agent.id)
    # print("Deleted agent")

    messages = project().agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
    

if __name__ == '__main__':
    main()