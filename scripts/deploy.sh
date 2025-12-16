#!/bin/bash
set -e

ENV=$1
echo "🚀 Deploying agents to $ENV environment"

# Example:
# az ai agent deploy --env $ENV --path agents/

echo "✅ Deployment to $ENV complete"
