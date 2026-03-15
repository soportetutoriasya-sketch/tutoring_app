## Features

   - **User Roles:** Student, Tutor, App Admin, Content Admin — each with dedicated dashboards
   - **Tutoring Sessions:** Full workflow — request, accept, complete, cancel, and review
   - **Geolocation:** Leaflet.js map integration for locating nearby tutors
   - **Tutor Reports:** Session reports with PDF and CSV export (via reportlab)
   - **Authentication:** django-allauth with email verification, login via username or email
   - **Internationalization:** English and Spanish (i18n ready)
   - **Dark/Light Mode:** Theme toggle with Bootstrap 5
   - **REST API:** djangorestframework for API endpoints
   - **Admin Panel:** Full Django admin with custom model management

   ## Tech Stack

   | Component       | Technology                       |
   |-----------------|----------------------------------|
   | Backend         | Django 5.2, Python 3.11+         |
   | Database        | PostgreSQL 15+                   |
   | Frontend        | Bootstrap 5, Leaflet.js          |
   | Authentication  | django-allauth                   |
   | Forms           | django-crispy-forms + bootstrap5 |
   | PDF Export      | reportlab                        |
   | Maps            | Leaflet.js, Google Maps API      |
   | Environment     | django-environ                   |

   ## Project Structure

   ```
   NewTutoringApp/
   ├── manage.py
   ├── requirements.txt
   ├── .env.example
   ├── tutoringApp/
   │   ├── settings/
   │   │   ├── base.py            # Shared settings
   │   │   ├── development.py     # Dev settings (DEBUG, local DB)
   │   │   └── production.py      # Production settings
   │   ├── apps/
   │   │   ├── accounts/          # User profiles, auth, signals
   │   │   ├── services/          # Sessions, subjects, reviews, reports
   │   │   ├── core/              # Home, about, contact pages
   │   │   ├── dashboard/         # Role-based dashboards, subject CRUD
   │   │   └── reports/           # PDF/CSV report generation
   │   ├── templates/             # All HTML templates
   │   ├── static/                # CSS, JS
   │   ├── fixtures/              # Initial data (subjects)
   │   └── locale/                # Translation files (en, es)
   ```

   ## Prerequisites

   - **Python 3.11+** — [Download](https://www.python.org/downloads/)
   - **PostgreSQL 15+** — see installation steps below
   - **Git** — [Download](https://git-scm.com/downloads)

   ---

   ## Step 1 — Install PostgreSQL

   ### Windows

   1. Download the installer from [https://www.enterprisedb.com/downloads/postgres-postgresql-downlo   
   ads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) (choose version 15 or    
   later).
   2. Run the installer:
      - Select all components (PostgreSQL Server, pgAdmin, Command Line Tools).
      - Set a password for the `postgres` superuser — **remember this password**.
      - Keep the default port `5432`.
      - Complete the installation.
   3. Open **pgAdmin** (installed with PostgreSQL) or a terminal and create the database:
      ```sql
      CREATE DATABASE tutoringapp;
      ```
      Using the command line:
      ```bash
      psql -U postgres
      # Enter your password when prompted
      CREATE DATABASE tutoringapp;
      \q
      ```

   ### macOS

   ```bash
   brew install postgresql@15
   brew services start postgresql@15
   createdb tutoringapp
   ```

   ### Linux (Ubuntu/Debian)

   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   sudo -u postgres psql
   ```
   Then inside psql:
   ```sql
   ALTER USER postgres WITH PASSWORD 'postgres';
   CREATE DATABASE tutoringapp;
   \q
   ```

   ---

   ## Step 2 — Clone the Repository

   ```bash
   git clone https://github.com/soportetutoriasya-sketch/tutoring_app.git
   cd tutoring_app
   ```

   ---

   ## Step 3 — Create and Activate Virtual Environment

   ### Windows (PowerShell)

   ```powershell
   python -m venv ven
   ven\Scripts\activate
   ```

   ### macOS / Linux

   ```bash
   python3 -m venv ven
   source ven/bin/activate
   ```

   ---

   ## Step 4 — Install Dependencies

   ```bash
   pip install -r requirements.txt
   ```

   ---

   ## Step 5 — Configure Environment Variables

   Copy the example file and edit it with your values:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your settings:

   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   GOOGLE_MAPS_API_KEY=your-google-maps-api-key
   ```

   **Important:** Update the database password in `tutoringApp/settings/development.py` if your        
   PostgreSQL `postgres` user password is not `postgres`:

   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": "tutoringapp",
           "USER": "postgres",
           "PASSWORD": "your-postgres-password",  # <-- change this
           "HOST": "localhost",
           "PORT": "5432",
       }
   }
   ```

   ---

   ## Step 6 — Run Migrations

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

   ---

   ## Step 7 — Load Initial Data

   ```bash
   python manage.py loaddata initial_subjects
   ```

   ---

   ## Step 8 — Create a Superuser

   ```bash
   python manage.py createsuperuser
   ```

   ---

   ## Step 9 — Run the Development Server

   ```bash
   python manage.py runserver
   ```

   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

   Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

   ---

   ## Troubleshooting

   | Problem | Solution |
   |---|---|
   | `password authentication failed for user "postgres"` | Update the password in `development.py`    
   to match your PostgreSQL password |
   | `relation "services_subject" does not exist` | Run `python manage.py makemigrations && python     
   manage.py migrate` |
   | `No fixture named 'initial_subjects' found` | Fixtures are loaded from `tutoringApp/fixtures/`    
   — ensure `FIXTURE_DIRS` is set in `base.py` |
   | `ModuleNotFoundError: No module named 'psycopg2'` | Run `pip install psycopg2-binary` |
   | `Could not connect to server` | Ensure PostgreSQL is running on port 5432 |
   ENDOFFILE
   Write README.md with proper UTF-8 encoding
