# 世界のごちそう — Django + PostgreSQL + Geoapify

## Setup (Windows / VS Code)
1. Open this folder in VS Code (the folder containing `manage.py`).
2. Create database `sekai_restaurant` in pgAdmin: Databases → Create → Database.
3. In VS Code PowerShell terminal:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:DB_NAME="sekai_restaurant"
$env:DB_USER="postgres"
$env:DB_PASSWORD="YOUR_REAL_POSTGRES_PASSWORD"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
python manage.py makemigrations restaurant
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Use your actual PostgreSQL password. If you open a new terminal, set the DB environment variables again.
4. Visit http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/.
5. In Admin, add Food menu items and upload images. Orders and reservations appear in Admin automatically.

## Geoapify
Get a key from https://myprojects.geoapify.com/ then set:
```powershell
$env:GEOAPIFY_API_KEY="YOUR_GEOAPIFY_API_KEY"
```
Restart the server. The map uses an OpenStreetMap tile fallback if no key is set. Sample coordinates are near Osaka Station and must be replaced with the actual restaurant location before publishing.

## Important
This is a learning/demo project. Orders are saved but online payments are not implemented. For public deployment, configure a secure secret key, DEBUG=False, ALLOWED_HOSTS, HTTPS, and environment secrets.
