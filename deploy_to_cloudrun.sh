#!/bin/bash

# Configuration
PROJECT_ID="antigravity-nexus-v1" # Replace with your actual Project ID
SERVICE_NAME="nexus-signal-server"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"
SOURCE_DIR="./bridge/SignallingWebServer"

echo "🚀 preparing to deploy Antigravity Nexus Signalling Server..."

# Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: Google Cloud SDK (gcloud) is not installed."
    echo "   Please install it: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "🔐 Checking Authentication..."
gcloud auth login --brief
gcloud auth configure-docker

echo "📦 Building Docker Image..."
# We need to run build from the directory containing Dockerfile to respect relative paths if any
# But based on inspection, it seems self-contained or expects bridge root.
# Trying bridge root context:
docker build -t $IMAGE_NAME -f $SOURCE_DIR/Dockerfile ./bridge

echo "⬆️ Pushing to Container Registry..."
docker push $IMAGE_NAME

echo "☁️ Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --project $PROJECT_ID \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --session-affinity \
    --timeout 3600 \
    --concurrency 80

echo "✅ Deployment Complete!"
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'
