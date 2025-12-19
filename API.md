


**API Specification**

### Base URL

`http://localhost:5000`

**Endpoints**

**1. /users/register**

* **Method:** POST
* **Purpose:** Register a new user.
* **Request Body:**

  ```json
  {
    "email": "student@example.com",
    "password": "password123"
  }
  ```
* **Response:**

  ```json
  {
    "message": "Registration successful"
  }
  ```
* **Error Codes:**

  * **400:** Invalid data (e.g., empty email or password).
  * **409:** Conflict (email already taken).

---

**2. /users/login**

* **Method:** POST
* **Purpose:** Log in a user.
* **Request Body:**

  ```json
  {
    "email": "student@example.com",
    "password": "password123"
  }
  ```
* **Response:**

  ```json
  {
    "message": "Login successful"
  }
  ```
* **Error Codes:**

  * **401:** Unauthorized (incorrect email or password).

---

**3. /users/profile**

* **Method:** GET
* **Purpose:** Retrieve current user profile information.
* **Response:**

  ```json
  {
    "id": 1,
    "email": "student@example.com",
    "name": "John Doe",
    "events": [
      {
        "event_id": 101,
        "name": "Robotics Workshop",
        "date": "2025-12-22"
      }
    ]
  }
  ```

---

**4. /events**

* **Method:** GET
* **Purpose:** Retrieve a list of all events.
* **Response:**

  ```json
  [
    {
      "id": 1,
      "name": "Robotics Workshop",
      "date": "2025-12-22",
      "location": "Room 101",
      "category": "Workshop"
    },
    {
      "id": 2,
      "name": "Book Club Meeting",
      "date": "2025-12-23",
      "location": "Library",
      "category": "Social"
    }
  ]
  ```

---

**5. /events/{event_id}**

* **Method:** GET
* **Purpose:** Retrieve detailed information about an event.
* **Request Parameters:**

  * `event_id`: ID of the event.
* **Response:**

  ```json
  {
    "id": 1,
    "name": "Robotics Workshop",
    "date": "2025-12-22",
    "location": "Room 101",
    "category": "Workshop",
    "description": "An exciting workshop on building robots using Arduino."
  }
  ```

---

**6. /events/register**

* **Method:** POST
* **Purpose:** Register for an event.
* **Request Body:**

  ```json
  {
    "event_id": 1
  }
  ```
* **Response:**

  ```json
  {
    "message": "Successfully registered for the event."
  }
  ```
* **Error Codes:**

  * **400:** Registration error (e.g., event not found).
  * **403:** Cannot register (e.g., user already registered).

---

**7. /clubs**

* **Method:** GET
* **Purpose:** Retrieve a list of all clubs.
* **Response:**

  ```json
  [
    {
      "id": 1,
      "name": "Robotics Club",
      "members_count": 15,
      "events": [
        {
          "event_id": 101,
          "name": "Robotics Workshop"
        }
      ]
    },
    {
      "id": 2,
      "name": "Book Club",
      "members_count": 25,
      "events": [
        {
          "event_id": 102,
          "name": "Book Club Meeting"
        }
      ]
    }
  ]
  ```

---

**8. /clubs/join**

* **Method:** POST
* **Purpose:** Send a request to join a club.
* **Request Body:**

  ```json
  {
    "club_id": 1
  }
  ```
 **Response:**

  ```json
  {
    "message": "Join request sent successfully."
  }
  ```
* **Error Codes:**

  * **400:** Request error (e.g., club not found).
  * **409:** User already a member of the club.

---

**9. /clubs/{club_id}**

* **Method:** GET
* **Purpose:** Retrieve detailed information about a club.
* **Request Parameters:**

  * `club_id`: ID of the club.
* **Response:**

  ```json
  {
    "id": 1,
    "name": "Robotics Club",
    "members_count": 15,
    "events": [
      {
        "event_id": 101,
        "name": "Robotics Workshop"
      }
    ]
  }
  ```

---

**10. /notifications**

* **Method:** GET
* **Purpose:** Retrieve a list of notifications for the current user.
* **Response:**

  ```json
  [
    {
      "id": 1,
      "message": "You have successfully registered for Robotics Workshop.",
      "date": "2025-12-20"
    },
    {
      "id": 2,
      "message": "Book Club Meeting is coming up on 2025-12-23.",
      "date": "2025-12-21"
    }
  ]
  ```

---

 **11. /admin/events**

* **Method:** POST
* **Purpose:** Admin creates a new event.
* **Request Body:**

  ```json
  {
    "name": "Robotics Workshop",
    "date": "2025-12-22",
    "location": "Room 101",
    "category": "Workshop",
    "description": "An exciting workshop on building robots using Arduino."
  }
  ```
* **Response:**

  ```json
  {
    "message": "Event created successfully."
  }
  ```


 **12. /admin/events/{event_id}**

* **Method:** PUT
* **Purpose:** Admin updates an event.
* **Request Parameters:**

  * `event_id`: ID of the event.
* **Request Body:**

  ```json
  {
    "name": "Updated Robotics Workshop",
    "date": "2025-12-23",
    "location": "Room 102",
    "category": "Workshop",
    "description": "Updated event description."
  }
  
 **Response:**

  ```json
  {
    "message": "Event updated successfully."
  }
  

Error Codes

 **400:** Bad request (e.g., missing required parameters).
 **401:** Unauthorized (missing or incorrect authentication token).
 **403:** Forbidden (e.g., user does not have permission to perform the action).
 **404:** Not found (e.g., the requested resource does not exist).
 **500:** Internal server error.
