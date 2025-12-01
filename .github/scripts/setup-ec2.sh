#!/bin/bash
set -e

echo "=== EC2 Setup Script ==="

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
  echo "Installing Docker..."
  sudo yum update -y
  sudo yum install -y docker
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo usermod -aG docker ec2-user
  echo "Docker installed successfully"
else
  echo "Docker is already installed"
fi

# Install AWS CLI if not already installed
if ! command -v aws &> /dev/null; then
  echo "Installing AWS CLI..."
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip -q awscliv2.zip
  sudo ./aws/install
  rm -rf aws awscliv2.zip
  echo "AWS CLI installed successfully"
else
  echo "AWS CLI is already installed"
fi

echo "=== EC2 Setup Complete ==="
