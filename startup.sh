#!/bin/bash
# This script is used to start the Flask application. 
# Utilize "./startup.sh" to run script.

# Step 1: Create necessary virtual environment (virtualenv) directory
echo "Creating virtual environment..."
source ./virtualenv/bin/activate

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 4: Set FLASK_APP environment variable (adjust if your entry point is different)
export FLASK_APP=wsgi.py

# Optional: Set FLASK_ENV to development if you want debug mode
export FLASK_ENV=development

# Step 5: Run the Flask application
echo "Starting Flask application..."
flask run
