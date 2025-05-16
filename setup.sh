#!/bin/bash
# setup_dev.sh

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Making migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser

echo "Populating database with sample questions..."
python manage.py populate_db

echo "Development setup complete!"
echo "Run the development server with: python manage.py runserver"