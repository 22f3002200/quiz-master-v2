# Quiz Master v2

Quiz Master v2 is a multi-user application that serves as an exam preparation platform. It has two main roles: Admin and User. Admins can manage the content of the platform, including subjects, chapters, quizzes, and questions. Users can take quizzes, view their scores, and track their progress.

## Features

### Admin 🛡️

  * **Manage Users:** Create, read, update, and delete users.
  * **Manage Subjects:** Create, read, update, and delete subjects.
  * **Manage Chapters:** Create, read, update, and delete chapters within subjects.
  * **Manage Quizzes:** Create, read, update, and delete quizzes within chapters.
  * **Manage Questions:** Create, read, update, and delete questions for each quiz.
  * **View Analytics:** View detailed analytics of quiz and user performance.
  * **Export Data:** Export quiz and user data to CSV files.

### User 👤

  * **Authentication:** Register and log in to the platform.
  * **Take Quizzes:** Attempt quizzes on various subjects and chapters.
  * **View Scores:** View detailed scores and performance on attempted quizzes.
  * **Review Answers:** Review the correct and incorrect answers after attempting a quiz.
  * **Track Progress:** View a dashboard with statistics and charts to track their progress.

## Tech Stack

### Frontend

  * **Vue.js:** A progressive JavaScript framework for building user interfaces.
  * **Vue Router:** The official router for Vue.js.
  * **Bootstrap:** A popular CSS framework for building responsive, mobile-first websites.
  * **Chart.js:** A simple yet flexible JavaScript charting library for designers & developers.

### Backend

  * **Flask:** A lightweight WSGI web application framework in Python.
  * **Flask-SQLAlchemy:** A Flask extension that provides an Object-Relational Mapper (ORM) for working with databases.
  * **Flask-JWT-Extended:** A Flask extension for adding JSON Web Tokens (JWT) to your application.
  * **Celery:** An asynchronous task queue/job queue based on distributed message passing.
  * **Redis:** An in-memory data structure store, used as a message broker for Celery and for caching.
  * **SQLite:** A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.

## Getting Started

### Prerequisites

  * Python 3.8+
  * Node.js and npm
  * Redis

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/quiz-master-v2.git
    cd quiz-master-v2
    ```
2.  **Backend Setup:**
    ```bash
    cd backend
    pip install -r requirements.txt
    flask run
    ```
3.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    npm run serve
    ```

## Project Structure

```
quiz-master-v2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── models/
│   │   ├── schema/
│   │   ├── __init__.py
│   │   └── ...
│   ├── run.py
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── router/
│   │   └── ...
│   ├── public/
│   └── ...
└── README.md
```

## Contributing

Contributions are welcome\! Please feel free to submit a pull request or open an issue if you find a bug or have a suggestion for a new feature.
