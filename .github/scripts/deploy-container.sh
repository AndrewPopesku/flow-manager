#!/bin/bash
set -e

IMAGE_NAME=${IMAGE_NAME:-flow-manager}
CONTAINER_PORT=${CONTAINER_PORT:-8000}
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
FULL_IMAGE="${ECR_REGISTRY}/${IMAGE_NAME}:latest"

echo "=== Container Deployment Script ==="
echo "Image: ${FULL_IMAGE}"
echo "Container: ${IMAGE_NAME}"
echo "Port: ${CONTAINER_PORT}"

# Login to ECR
echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region "${AWS_REGION}" | \
  sudo docker login --username AWS --password-stdin "${ECR_REGISTRY}"

# Pull latest image
echo "Pulling latest image..."
sudo docker pull "${FULL_IMAGE}"

# Stop and remove old container if exists
echo "Stopping old container (if exists)..."
sudo docker stop "${IMAGE_NAME}" 2>/dev/null || true
sudo docker rm "${IMAGE_NAME}" 2>/dev/null || true

# Run new container
echo "Starting new container..."
sudo docker run -d \
  --name "${IMAGE_NAME}" \
  -p "${CONTAINER_PORT}:${CONTAINER_PORT}" \
  --restart unless-stopped \
  "${FULL_IMAGE}"

echo "=== Deployment Complete ==="
echo "Container ${IMAGE_NAME} is running on port ${CONTAINER_PORT}"
