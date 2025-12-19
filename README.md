Campus Event Navigator
Overview

Campus Event Navigator is a website designed to help SDU students manage and stay up-to-date with campus events, club activities, and academic deadlines in one central platform. The app allows students to explore upcoming events, track their participation, and receive personalized reminders, ensuring they never miss important activities.

This platform also benefits university administrators by providing them with tools to manage events more efficiently and boost overall campus engagement.

Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Flask, Python
Database: SQLite
Tools: Flask-SQLAlchemy, Flask-Login, Flask-WTF

Project Structure
The project is structured as follows:
/pycache – Contains Python bytecode cache files.
/instance – Contains configuration and runtime data for the application.
/migrations – Includes database migration files.
/static – Holds static files like CSS, images, JavaScript, etc.
/templates – Contains the HTML templates used by Flask.
.DS_Store – Mac-specific metadata file.
README.md – Project documentation (this file).
app.py – The main Flask application file, handling routing and server logic.
forms.py – Contains form definitions for user registration, login, and other interactions.
requirements.txt – A file listing all required Python dependencies

How to Run the Project
System Requirements:
Python 3.x
SQLite (for local database storage)

Installation Steps:

Clone the repository:
git clone https://github.com/yourusername/campus-event-navigator.git


Install the dependencies:
pip install -r requirements.txt


Set up the database:
flask db upgrade


Run the project locally:
flask run

How to Run Tests
To run the tests, use the following command:
pytest

Additional Documents
PRD.md
User Stories.md
Architecture.md
API.md