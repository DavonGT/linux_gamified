@echo off
:: setup.bat - Windows setup script for Django project

:: Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment
        exit /b 1
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies
    exit /b 1
)

echo Making migrations...
python manage.py makemigrations
if %ERRORLEVEL% NEQ 0 (
    echo Failed to make migrations
    exit /b 1
)

python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo Failed to apply migrations
    exit /b 1
)

echo Creating superuser...
python manage.py createsuperuser
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create superuser
    exit /b 1
)

echo Populating database with sample tasks...
python manage.py populate_db
if %ERRORLEVEL% NEQ 0 (
    echo Failed to populate database
    exit /b 1
)

echo Development setup complete!
echo Run the development server with: python manage.py runserver

:: Keep the window open to see the output
pause