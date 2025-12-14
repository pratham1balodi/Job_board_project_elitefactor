# 🚀 Job Board Pro: Your Next Career Connection

Welcome to the Job Board Pro project! This is a complete, full-stack web application built with **Django** that facilitates the entire hiring workflow, from job posting to application tracking.

The goal of this project was to implement distinct user roles and comprehensive management features, making it a robust, real-world application.

## 🌟 Key Features at a Glance

| Feature | User Role | Status |
| :--- | :--- | :--- |
| **Authentication** | All | Secure Login & Seeker/Employer Sign-up |
| **Job Posting** | Employer | Create new job listings |
| **Advanced Search** | Seeker/Guest | Filter jobs by Title, Location, and Category |
| **Job Application** | Job Seeker | One-click application; blocks duplicates |
| **Applicant Tracking** (ATS) | Employer | View applicants per job and update their status (e.g., Interview, Hired) |
| **Dashboards** | All | Dedicated management views for Seeker (status tracking) and Employer (analytics) |
| **Management** | Employer | Edit and Archive (Deactivate) existing job listings |

## 🛠️ Project Setup: Get Running in 5 Minutes

Follow these simple steps to get the Job Board Pro server up and running on your local machine.

### 1. Prerequisites

You must have Python 3.x and pip installed.

### 2. Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR GITHUB LINK HERE]
    cd job_board_project_final
    ```

2.  **Set Up Virtual Environment & Install Dependencies:**
    It's best practice to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Database Migration:**
    We use SQLite (or PostgreSQL, if you configured it) for the database. Run the necessary setup commands:
    ```bash
    python manage.py migrate
    ```

4.  **Create an Admin Account (Superuser):**
    This account allows you to manage all users and jobs via the admin panel.
    ```bash
    python manage.py createsuperuser
    ```

5.  **Launch the Server!**
    ```bash
    python manage.py runserver
    ```
    Your application will be live at: `http://127.0.0.1:8000/`

## 🔑 Testing & Access Points

To test the full workflow, you need to create accounts for each role:

| User Role | Entry Point | Purpose |
| :--- | :--- | :--- |
| **Guest/Seeker** | `/jobs/` | Search and view listings. |
| **Job Seeker** | `/accounts/signup/seeker/` | Register, then apply for jobs. View application status at `/jobs/dashboard/seeker/`. |
| **Employer** | `/accounts/signup/employer/` | Register, then post jobs at `/jobs/post/`. Manage applicants at `/jobs/dashboard/employer/`. |
| **Admin** | `/admin/` | Manage all database objects. |

---

## 📜 Evaluation Notes (For the Grader)

* **Technology:** Built using Django (Python), Bootstrap 5 (Frontend), and SQLite (Database).
* **Best Practices:** Implements Class-Based Views (CBVs), custom `User` model, role-based access control, and secure form handling.
* **Database File:** The `db.sqlite3` file is included in the submission folder.
* **Dependencies:** All required packages are listed in `requirements.txt`.
