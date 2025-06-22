Sure! Here's your entire **Quiz Master - V2** project statement converted into **Markdown format**:

---

# Modern Application Development II

## Project Statement

## Quiz Master - V2

> A multi-user app that serves as an exam preparation platform for multiple courses, with Admin and User roles.

---

## Frameworks to be Used (Mandatory)

* **SQLite** for data storage
* **Flask** for API
* **VueJS** for UI
* **VueJS Advanced with CLI** (Only if required)
* **Jinja2** templates (Only for entry point via CDN; not for UI)
* **Bootstrap** for HTML generation and styling
  ❌ No other CSS framework allowed
* **Redis** for caching
* **Redis + Celery** for batch jobs

> ⚠️ All demos must run on your local machine.

---

## User Roles

### 🛡️ Admin (Quiz Master)

* Root access (superuser)
* No registration required
* Only **one** admin account exists
* Redirects to Admin Dashboard upon login

**Admin Capabilities:**

* Manage users
* Create and manage:

  * Subjects
  * Chapters under subjects
  * Quizzes under chapters
  * Questions under quizzes

### 👤 User

* Can register and login
* Can attempt any quiz of interest
* Can view quiz scores

**User Fields:**

* `id`: Primary key
* `Username` (email)
* `Password`
* `Full Name`
* `Qualification`
* `DOB`

---

## Terminologies

### 📚 Subject

* Created by Admin
* Fields:

  * `id`: Primary key
  * `Name`
  * `Description`
  * Additional fields as needed

### 🧾 Chapter

* Subdivision of a subject
* Fields:

  * `id`: Primary key
  * `Name`
  * `Description`
  * Additional fields as needed

### 🧪 Quiz

* A test under a chapter
* Fields:

  * `id`: Primary key
  * `chapter_id`: FK to Chapter
  * `date_of_quiz`
  * `time_duration` (HH\:MM)
  * `remarks` (optional)
  * Additional fields as needed

### ❓ Questions

* Part of a quiz
* Fields:

  * `id`: Primary key
  * `quiz_id`: FK to Quiz
  * `question_statement`
  * `option1`, `option2`, ... (Only one correct)

### 🧮 Scores

* Records user's quiz performance
* Fields:

  * `id`: Primary key
  * `quiz_id`: FK to Quiz
  * `user_id`: FK to User
  * `time_stamp_of_attempt`
  * `total_scored`
  * Additional fields as needed

> ✅ You may add more fields as needed.

---

## Application Wireframe

> Wireframes are for reference only.
> Feel free to design your own frontend while preserving the required flow and functionality.

---

## Core Functionalities

### 🔐 Authentication

* Login/Register for Users
* Login for Admin only (admin role is pre-defined)
* Role-based access control using:

  * Flask session/token
  * OR JWT-based auth

### 🛠️ Admin Dashboard

* Pre-inserted admin in DB on app init
* CRUD for:

  * Subjects
  * Chapters under subjects
  * Quizzes under chapters
  * Questions (MCQs - single correct answer)
* Search: users, subjects, quizzes
* Summary charts

### 📝 Quiz Management (Admin)

* Edit/delete quizzes
* Set date and duration
* Create/edit/delete MCQ questions

### 📊 User Dashboard

* Attempt quizzes of interest
* Quiz timer
* Record scores
* View past attempts
* View summary charts

> ⚠️ Database must be created programmatically. No manual DB setup allowed (e.g., DB Browser for SQLite not permitted).

---

## Backend Jobs

### ⏰ a. Scheduled Job - Daily Reminders

* Notify users via Google Chat Webhook / SMS / Email
* Triggers if:

  * User has been inactive
  * New quiz created relevant to user
* Schedule: Evening (customizable)

### 📅 b. Scheduled Job - Monthly Activity Report

* Auto-generated report via HTML (or PDF)
* Sent via email on 1st day of each month
* Report includes:

  * Quizzes taken
  * Scores
  * Average score
  * Ranking

### 📥 c.1 User-Triggered Async Job - Export User Quiz Details

* CSV export of:

  * quiz\_id, chapter\_id, date\_of\_quiz, score, remarks
* Dashboard trigger
* Background job with alert on completion

**OR**

### 📥 c.2 Admin-Triggered Async Job - Export All Quiz Details

* CSV export of:

  * user\_id, quizzes\_taken, average\_score
* Dashboard trigger
* Background job with alert on completion

---

## 🧠 Performance and Caching

* Use Redis for performance improvement
* Apply cache expiry
* Optimize API performance

---

## ✅ Recommended Functionalities

* Well-designed **PDF reports** (monthly reports)
* Use **ChartJS** or similar for analytics
* **Responsive UI**:

  * Works across devices
  * Add-to-desktop feature
* **Frontend Validation**:

  * HTML5 or JavaScript-based
* **Backend Validation**:

  * Within Flask APIs

---

## 🌟 Optional Functionalities

* Aesthetic frontend using Bootstrap
* Secure login using:

  * `flask_login`, `flask_security`, etc.
* Dummy payment portal view (for paid quizzes)
* Any additional feature you think is relevant

---

Let me know if you want a downloadable `.md` file or need this formatted into a document or presentation.
