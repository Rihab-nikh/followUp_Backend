Seed scripts
=================

How to run
----------

1. Activate your project's virtual environment (or use absolute python path).

   In PowerShell (from project root):

   & .venv\Scripts\Activate.ps1

2. Run the seed script from the project package root so imports resolve:

   & .venv\Scripts\python.exe .\extracted_backend\extracted_backend\followup-backend\scripts\seed_db.py

What it does
------------

- Creates 3 users with French names/roles.
- Creates example companies, meetings, tasks, notifications, AI chat and KPI metrics.
- Attempts to connect to MongoDB using `MONGO_URI` from environment; if unavailable it uses the project's mock in-memory DB.

Notes
-----
- Password for seeded users is 'Passw0rd!'. Passwords are hashed using bcrypt.
- Running the script multiple times will clear and re-seed the collections listed in the script.

Testing API endpoints from PowerShell / curl / Python
---------------------------------------------------

This section contains short examples to test the backend's auth/login endpoint from Windows (PowerShell) and from environments where curl is available.

1) PowerShell (recommended)

- Quick one-liner using Invoke-RestMethod (returns parsed JSON):

```powershell
$body = @{ email = 'abla.benslimane@axians.com'; password = 'Leviathan@123*' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/auth/login' -Method Post -Body $body -ContentType 'application/json'
```

- Or use the helper script included in this folder (reads env vars if parameters are omitted):

```powershell
# set env vars (optional)
$env:TEST_USER_EMAIL = 'abla.benslimane@axians.com'
$env:TEST_USER_PASSWORD = 'Leviathan@123*'

# run the helper
.\test_login.ps1
# or provide parameters
.\test_login.ps1 -Email 'abla.benslimane@axians.com' -Password 'Leviathan@123*'
```

2) curl (use curl.exe on Windows to avoid PowerShell aliasing)

```powershell
curl.exe -i -X POST "http://127.0.0.1:5000/api/auth/login" -H "Content-Type: application/json" -d "{\"email\":\"abla.benslimane@axians.com\",\"password\":\"Leviathan@123*\"}"
```

3) Python requests

```powershell
& .venv\Scripts\python.exe -c "import requests; r=requests.post('http://127.0.0.1:5000/api/auth/login', json={'email':'abla.benslimane@axians.com','password':'Leviathan@123*'}); print(r.status_code); print(r.text)"
```

Notes
- PowerShell's `curl` is an alias for `Invoke-WebRequest`/`Invoke-RestMethod`; use `curl.exe` to call the real curl binary.
- Avoid using Bash-style heredocs (`<<'PY'`) in PowerShell; they are not supported. Use here-strings or run a temporary script file instead.
- Keep credentials out of repo files in general. Use environment variables for safer local testing.
