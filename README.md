# Student Management System (Flask)

A beginner-friendly full-stack CRUD website using Flask, SQLite, HTML, CSS and Jinja.

## Run on Windows

1. Install Python 3.10 or newer.
2. Open Command Prompt in this folder.
3. Create a virtual environment:

   `py -m venv .venv`

4. Activate it:

   `.venv\\Scripts\\activate`

5. Install dependencies:

   `python -m pip install -r requirements.txt`

6. Start the website:

   `python -m flask --app app run --debug`

7. Open http://127.0.0.1:5000 in your browser.

The SQLite database is created automatically the first time the app starts.
The local database file is ignored by Git so student records are not uploaded.

## Important before deployment

- Set a strong random `SECRET_KEY` environment variable.
- Turn off debug mode in production.
- Add CSRF protection, authentication and authorization before using real student data.
- Use a managed production database and HTTPS for a public deployment.
