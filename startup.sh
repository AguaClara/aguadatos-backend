#!/bin/bash
# This script is used to install necessary dependencies and start the Flask application. 
# Utilize "./startup.sh" to run script.

# Step 0: Ensure 'instance' directory is created to house database file
if [ ! -d "instance" ]; then
    echo "Creating 'instance' directory..."
    mkdir instance
fi

# Step 1: Create necessary virtual environment (virtualenv) directory if not created yet
echo "Creating virtual environment..."
if [ ! -d "virtualenv" ]; then
    echo "Creating virtual environment directory..."
    python3 -m venv virtualenv
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source ./virtualenv/bin/activate

# Step 3: Install dependencies from requirements.txt if not installed yet
echo "Installing dependencies from requirements.txt..."
pip3 install -r requirements.txt

# Step 4: Set FLASK_APP environment variable (adjust if your entry point is different)
export FLASK_APP=wsgi.py

# Optional: Set FLASK_ENV to development if you want debug mode
export FLASK_ENV=development

# Step 5: Run the Flask application
echo "Starting Flask application..."
flask run

# Step 6: Delete the aguadatos.db file upon exiting the application
echo "Deleting aguadatos database file..."
rm instance/aguadatos.db