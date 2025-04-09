#!/bin/bash

API_URL=$1

if [ -z "$API_URL" ]; then
  echo "Usage: ./set-api-url.sh <API_URL>"
  exit 1
fi

echo "Setting API URL in .env..."
echo "VITE_API_BASE_URL=$API_URL" > mental-health-frontend/.env

echo " .env updated to:"
cat mental-health-frontend/.env
