from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

def project():
    project_connection_string="eastus.api.azureml.ms;679e680;ai;devy"

    project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string,
    credential=DefaultAzureCredential())
    
    return project

def search():
    # Configure inference/search
    openai = project().inference.get_azure_openai_client(api_version="2024-06-01")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You help me with Kubernetes Event-Drive Autoscaling"},
            {"role": "user", "content": "Tell me how to programmatically create a KEDA Cron Job for a Pod"},
        ]
    )

    print(response.choices[0].message.content)


search()