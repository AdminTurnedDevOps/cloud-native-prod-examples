terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# IAM role for Karpenter
resource "aws_iam_role" "karpenter" {
  name = "karpenter-role${var.cluster_name}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${var.oidc_provider_url}"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${var.oidc_provider_url}:sub": "system:serviceaccount:karpenter:karpenter",
            "${var.oidc_provider_url}:aud": "sts.amazonaws.com"
          }
        }
      }
    ]
  })
}

# Get AWS account ID for IAM role
data "aws_caller_identity" "current" {}

# Karpenter controller policy
resource "aws_iam_policy" "karpenter" {
  name        = "KarpenterControllerPolicy-${var.cluster_name}"
  description = "IAM policy for Karpenter controller"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateFleet",
          "ec2:CreateLaunchTemplate",
          "ec2:CreateTags",
          "ec2:DeleteLaunchTemplate",
          "ec2:DescribeAvailabilityZones",
          "ec2:DescribeImages",
          "ec2:DescribeInstances",
          "ec2:DescribeInstanceTypeOfferings",
          "ec2:DescribeInstanceTypes",
          "ec2:DescribeLaunchTemplates",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeSubnets",
          "ec2:RunInstances",
          "ec2:TerminateInstances",
          "ec2:DescribeInstanceStatus",
          "iam:PassRole",
          "ssm:GetParameter"
        ]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["eks:DescribeCluster"]
        Resource = "arn:aws:eks:*:*:cluster/${var.cluster_name}"
      }
    ]
  })
}

# Attach the policy to the Karpenter role
resource "aws_iam_role_policy_attachment" "karpenter" {
  role       = aws_iam_role.karpenter.name
  policy_arn = aws_iam_policy.karpenter.arn
}

# Instance profile for Karpenter nodes
resource "aws_iam_instance_profile" "karpenter" {
  name = "KarpenterNodeInstanceProfile-${var.cluster_name}"
  role = aws_iam_role.karpenter.name
}

# Output the IAM role ARN
output "karpenter_role_arn" {
  description = "ARN of the IAM role for Karpenter"
  value       = aws_iam_role.karpenter.arn
} 