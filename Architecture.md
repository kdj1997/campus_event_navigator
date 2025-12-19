System Architecture
1. Architecture Style

The system follows a client-server architecture, where the client-side interacts with the server-side to retrieve and display data. The architecture is monolithic, with both the front end and back end packaged into a single application. Flask handles the routing and business logic, and the SQLite database stores user, event, and club data.

Reason for this choice:

Client-server allows for clear separation of concerns between the front end and back end.

Monolithic structure is suitable for a small to medium-scale application, making it easy to maintain and scale as needed.

2. System Components
Front end:

Technology: HTML, CSS, JavaScript

Responsibility: Displays pages such as the homepage, login, event listings, club registration, notifications, and user profiles. Uses simple, minimalistic designs for quick and responsive user interaction.

Back end:

Technology: Flask (Python)

Responsibility: Handles routing, user authentication, event management, and communication with the database. Manages business logic, such as generating event lists, sending notifications, and managing user profiles.

Database:

Technology: SQLite

Responsibility: Stores user data, club events, event sign-ups, and notification data. It supports the queries needed to fetch user-specific data (e.g., events a student has signed up for, user preferences).

External services:

Flask-SQLAlchemy: Used to interact with the database in an ORM (Object Relational Mapping) fashion, simplifying database operations.

Flask-Login: Manages user sessions and authentication.

Flask-WTF: Used for web forms and validation (e.g., user registration, event creation).

3. Component Diagram

![alt text](image.png)

Explanation:

Frontend: The user interacts with the frontend through a web browser.

Backend (Flask): Flask processes the requests, performs the necessary logic (e.g., querying events or registering a user), and sends responses back to the frontend.

Database (SQLite): Flask queries the SQLite database for event data, user profiles, and notifications. It updates the database when a new event is added or when a user signs up for an event.

4. Data Flow

User Action: A student logs into the system.

Frontend Request: The frontend sends a request to the backend for the user’s event data.

Backend Processing: Flask processes the request, interacts with the SQLite database to retrieve the necessary data (e.g., events the user is interested in), and prepares the response.

Response: Flask sends the data back to the frontend, which renders the event list on the user's dashboard.

User Interaction: The user selects an event to join, and the system updates the event participation status in the database.

5. Database Schema

User Table:

id (Primary Key)

email (Unique)

password (Encrypted)

name

role (e.g., student, admin)

Event Table:

id (Primary Key)

title

description

date

time

location

creator_id (Foreign Key linking to User)

Club Table:

id (Primary Key)

name

description

admin_id (Foreign Key linking to User)

UserEvent Table (Many-to-many relationship):

user_id (Foreign Key linking to User)

event_id (Foreign Key linking to Event)

status (e.g., signed-up, pending)

Notification Table:

id (Primary Key)

user_id (Foreign Key linking to User)

message

timestamp

6. Technology Decisions
Flask:

Chosen for its simplicity and flexibility in creating RESTful APIs and handling web requests. It is lightweight and well-suited for the scale of this project.

SQLite:

A lightweight and simple-to-set-up database system that works well for small projects. It’s appropriate for handling student and event data with minimal overhead.

Flask-SQLAlchemy:

This extension provides an ORM (Object Relational Mapping) system, making database interactions easy and reducing boilerplate SQL code.

Flask-Login:

Used for managing user authentication and sessions, allowing secure login, session tracking, and protection of user-specific routes.

Flask-WTF:

Simplifies form handling and validation, making user input (like event registration or login) secure and error-free.

7. Future Extensions

Push Notifications: For real-time event updates and reminders.

External Calendar Integration: Sync events with external calendar platforms like Google Calendar.

Event Filtering: More advanced filtering by categories, interests, and locations.

Social Media Integration: Allow students to share their events or achievements on social media platforms.

Mobile Version: Develop a mobile app for more convenient access to campus events and notifications.