# GIP Web

This is a Django web application for property listings.

## Setup

1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
   Then open `http://localhost:8000/` in your browser.

## Usage

- Visit `/` for the homepage and `/properties/` for property listings.
- The admin interface is available at `/admin/` when the server is running.
- The login page is available at `/login/` and will redirect back to the page you were viewing after authentication.

