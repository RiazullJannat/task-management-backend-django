# Task Management & Annotation Tool - Backend (Django)

## 🐉 The Saga & The Villains I Faced
This project required me to work with a completely new framework: Django. As my very first time using Django, I spent the first 2–3 days purely dedicated to learning its core concepts. The initial steep learning curve—understanding the ORM, configuring the environment correctly, and architecting normalized models for tasks, projects, and complex annotations—was the primary "villain" of this backend saga. 

However, by the grace of Almighty, I quickly grasped the basics and completed the backend successfully. Relying on the power of friendship with the official Django documentation, insightful blog posts, and AI assistance, I conquered the learning curve. While I am still building an in-depth understanding, I am confident that working on it further will sharpen my skills in no time.

## 🛠 Prerequisites
- **Python Version**: Python 3.10 or higher
- **Node Version**: Not required for the backend directly, but Node 18+ or 20+ is required for the Next.js frontend companion.

## 🚀 How to Run the Backend Project

1. **Clone the repository and navigate to the backend directory:**
   ```bash
   git clone <your-repo-url>
   cd task-management-backend-django
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On Linux/Mac:
   python3 -m venv .venv
   source .venv/bin/activate
   
   # On Windows:
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   - Ensure your `.env` file is present in the root directory (alongside `manage.py`) with your secret keys, database credentials, and any third-party API keys (like ImgBB for image hosting).

5. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   The backend will now be running at `http://127.0.0.1:8000/`.
