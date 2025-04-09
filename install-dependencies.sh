#!/bin/bash

echo "Installing backend dependencies..."
cd mental-health-backend || exit
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
deactivate
cd ..

echo "Installing frontend dependencies..."
cd mental-health-frontend || exit
npm install
cd ..

echo "All dependencies installed!"
