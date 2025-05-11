from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

fileLocation = '../../../../Users/michael/Downloads/Azure_AI_Foundry_Managed_GenAI_Breakdown.pdf'

def project():
    project_connection_string="eastus.api.azureml.ms;686b24a1-5707-4415-be01-f2b6e879e680;ai;devtestfoundry"

    project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string,
    credential=DefaultAzureCredential())
    
    return project

def main():
    document = [
        {
            "id": "1",
            "content": fileLocation
        }
    ]
    
    # Create a client to run search queries
    search_client = SearchClient(
        index_name="affable-deer-c43p4p9vyk",
        endpoint='https://test11111111.search.windows.net',
        credential=AzureKeyCredential(key='xxxxxx')
    )
    
    search_client.upload_documents(documents=document)
    
main()