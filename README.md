# Linux Gamified

## Project Overview

Linux Gamified is a Django-based web application designed to teach users about Linux commands and terminal navigation in a fun and interactive way.

## Features

* Interactive terminal simulation
* Variety of Linux commands to learn and practice
* Different game modes, including practice and timed modes
* Score tracking and leaderboard
* Customizable game settings

## Technologies Used

* Django (Python web framework)
* HTML/CSS (front-end development)
* JavaScript (front-end development)
* SQLite (database management)

## Installation

1. Clone the repository: `git clone https://github.com/DavonGT/linux-gamified.git`
2. Navigate to the project directory: `cd linux-gamified`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the migrations: `python manage.py migrate`
5. Make a super user account: `python manage.py createsuperuser`
6. Start the development server: `python manage.py runserver`
7. Go to admin page: `localhost:8000/admin/`
8. Add Tasks/Task(manually or via excel upload)

## Project Structure

* `linux_gamified/`: Project root directory
	+ `settings.py`: Project settings
	+ `urls.py`: URL configuration
* `game/`: Game application directory
	+ `models.py`: Game models
	+ `views.py`: Game views
	+ `templates/`: Game templates
	+ `static/`: Game static files
* `accounts/`: Accounts application directory
	+ `models.py`: Accounts models
	+ `views.py`: Accounts views
	+ `templates/`: Accounts templates
	+ `static/`: Accounts static files

