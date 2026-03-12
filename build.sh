set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## `Procfile` create kar

**Same folder madhe** (`manage.py` shejari) nava file banav:

**File name:** `Procfile` ← exactly hech naam, no extension, capital P

**`Procfile` madhe he paste kar:**
```
web: gunicorn clinic_appointment.wsgi:application