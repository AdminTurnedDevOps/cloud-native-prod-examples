from claude_code_sdk import query, ClaudeCodeOptions
from pathlib import Path
import anyio

async def main():

    options = ClaudeCodeOptions(
        max_turns=3,
        system_prompt="You are a Terraform expert. Your task is to create Terraform scripts based on user requests.",
        cwd=Path("../../terraform"),  # Can be string or Path
        allowed_tools=["Read", "Write", "Bash", "Python", "Zsh"],
        permission_mode="acceptEdits",
        model="claude-3-7-sonnet-latest",
        mcp_servers={
            "awslabs.eks-mcp-server": {
                "command": "uvx",
                "args": ["@aws/mcp-server-eks", "--allow-write"],
                "env": {
                    "AWS_REGION": "us-west-2",
                    "AWS_PROFILE": "default",
                }
            }
        }
    )
        
    async for message in query(prompt="""Within the `terraform` directory, create me a Terraform Module for creating Azure Virtual Machines (VM).
                                         This module should be as agnostic as possible, so heavy use on variables and passing in values to said variables at runtime.
                                         The module should have the ability to create more than one VM at a time.
                                         No Resource Group, vNet, or subnets need to be created, but variables need to exist so they can be passed in at runtime.
                                         There should be a variable to pass in the Azure subscription ID at runtime.
                                         The server Operating System that will be used in Windows Server 2022.
                                         The default size for the VM should be Standard B2.
                                         A Storage Account called `adtfstate` will be where the
                                         Terraform State is stored, so that should be in the backend configuration.""",
                               options=options):
        print(message)
        
if __name__ == "__main__":
    anyio.run(main)