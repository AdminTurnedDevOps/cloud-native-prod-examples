# Karpenter IAM for EKS

This Terraform configuration creates the IAM role and policy required for Karpenter to function with Amazon EKS.

## Usage

1. Initialize Terraform:
```bash
terraform init
```

2. Create a `terraform.tfvars` file:
```hcl
region           = "us-west-2"
cluster_name     = "my-eks-cluster"
oidc_provider_url = "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLEID"  # Without https://
```

3. Apply the configuration:
```bash
terraform apply
```

4. Use the role ARN output when installing Karpenter in your EKS cluster