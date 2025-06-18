# -*- mode: just -*-
# Justfile for Terraform operations
# Usage: just <command> [arguments]

# Default variables
env := "dev"
region := "us-west-2"

# Default recipe to run when just is called without arguments
default:
    @just --list

# Initialize Terraform with backend configuration
init env="dev" region=region:
    @echo "Initializing Terraform for {{ env }} environment in {{ region }} region..."
    terraform init -reconfigure \
        -backend-config="key=terraform/state/{{ env }}/terraform.tfstate"

# Format Terraform files
fmt:
    @echo "Formatting Terraform files..."
    terraform fmt -recursive

# Validate Terraform configuration
validate: fmt
    @echo "Validating Terraform configuration..."
    terraform validate

# Show plan for Terraform changes
plan env=env region=region:
    @echo "Planning Terraform changes for {{ env }} environment in {{ region }} region..."
    terraform plan -var="region={{ region }}" \
        -var-file="config/{{ env }}.tfvars" \
        -out="tfplan"

# Apply Terraform changes
apply:
    @echo "Applying Terraform changes..."
    terraform apply "tfplan"

# Apply Terraform changes without a saved plan (use with caution)
apply-direct env=env region=region:
    @echo "Applying Terraform changes directly for {{ env }} environment in {{ region }} region..."
    terraform apply -auto-approve \
        -var="region={{ region }}" \
        -var-file="config/{{ env }}.tfvars"

# Destroy resources created by Terraform
destroy env=env region=region:
    @echo "Destroying Terraform-managed infrastructure for {{ env }} environment in {{ region }} region..."
    terraform destroy \
        -var="region={{ region }}" \
        -var-file="config/{{ env }}.tfvars"

# Run Terraform state operations
state cmd="list":
    @echo "Running Terraform state {{ cmd }}..."
    terraform state {{ cmd }}

# Create workspace directories and files for a new environment
setup-env env="dev":
    @echo "Setting up environment structure for {{ env }}..."
    mkdir -p config
    @if [ ! -f "config/{{ env }}.tfvars" ]; then \
        echo "# Terraform variables for {{ env }} environment" > "config/{{ env }}.tfvars"; \
        echo "cluster_name = \"{{ env }}-cluster\"" >> "config/{{ env }}.tfvars"; \
        echo "region = \"us-west-2\"" >> "config/{{ env }}.tfvars"; \
        echo "# Add more variables as needed" >> "config/{{ env }}.tfvars"; \
        echo "Created config/{{ env }}.tfvars file"; \
    else \
        echo "config/{{ env }}.tfvars already exists"; \
    fi

# Clean Terraform files (use with caution)
clean:
    @echo "Cleaning Terraform files..."
    rm -rf .terraform/ tfplan terraform.tfstate*

# Install required tools
install-tools:
    @echo "Checking and installing required tools..."
    @if ! command -v terraform &> /dev/null; then \
        echo "Installing Terraform..."; \
        brew install terraform; \
    else \
        echo "Terraform is already installed"; \
    fi
    @terraform version

# Run security scan on Terraform code
scan:
    @echo "Running security scan on Terraform code..."
    @if ! command -v tfsec &> /dev/null; then \
        echo "Installing tfsec..."; \
        brew install tfsec; \
    fi
    tfsec .

# Create a workspace and switch to it
workspace-create name:
    @echo "Creating and switching to workspace {{ name }}..."
    terraform workspace new {{ name }} || terraform workspace select {{ name }}

# List available workspaces
workspace-list:
    @echo "Listing available Terraform workspaces..."
    terraform workspace list

# Update Terraform documentation 
docs:
    @echo "Updating Terraform documentation..."
    @if ! command -v terraform-docs &> /dev/null; then \
        echo "Installing terraform-docs..."; \
        brew install terraform-docs; \
    fi
    terraform-docs markdown . > TERRAFORM.md

# Create AWS Karpenter IAM role for an EKS cluster
create-karpenter-role cluster_name region=region:
    @echo "Creating Karpenter IAM role for {{ cluster_name }} in {{ region }}..."
    terraform apply -target=aws_iam_role.karpenter \
        -target=aws_iam_policy.karpenter \
        -target=aws_iam_role_policy_attachment.karpenter \
        -target=aws_iam_instance_profile.karpenter \
        -var="cluster_name={{ cluster_name }}" \
        -var="region={{ region }}"
