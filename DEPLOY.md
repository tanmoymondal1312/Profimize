# Profimize — cPanel Deployment Guide

## Prerequisites
- cPanel with **Setup Python App** (Phusion Passenger)
- MySQL database access
- Terminal or SSH access (recommended), or cPanel *Terminal* tool

---

## Step 1 — Create MySQL Database

1. cPanel → **MySQL Databases**
2. Create a new database, e.g. `cpaneluser_profimize`
3. Create a new user, e.g. `cpaneluser_dbuser` with a strong password
4. **Add user to database** → grant **ALL PRIVILEGES**
5. Note the full prefixed names (cPanel prepends your account username)

---

## Step 2 — Upload Code

### Option A — File Manager
1. On your local machine, zip the project:
   ```bash
   zip -r profimize.zip . \
     --exclude "*.pyc" \
     --exclude "__pycache__/*" \
     --exclude "venv/*" \
     --exclude ".env" \
     --exclude "staticfiles/*" \
     --exclude "media/*" \
     --exclude "db.sqlite3"
   ```
2. cPanel → **File Manager** → navigate to a folder **outside** `public_html`,
   e.g. `/home/cpaneluser/profimize/`
3. Upload the zip, then **Extract**

### Option B — Git Version Control
cPanel → **Git™ Version Control** → Create → point to your repo URL

---

## Step 3 — Setup Python App

1. cPanel → **Setup Python App** → **Create Application**
   - **Python version**: 3.11 (or highest 3.10+)
   - **Application root**: `profimize` (the folder you uploaded to, relative to home)
   - **Application URL**: your domain, e.g. `profimize.com`
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`
2. Click **Create**. cPanel generates a virtualenv and shows an activation command.

---

## Step 4 — Environment Variables

**Option A — cPanel Python App env vars UI:**
Add each key/value from `.env.example` in the UI.

**Option B — .env file:**
Create `/home/cpaneluser/profimize/.env` in File Manager with the real values.

Key settings for production:
```
DEBUG=False
SECRET_KEY=<generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
ALLOWED_HOSTS=profimize.com,www.profimize.com
CSRF_TRUSTED_ORIGINS=https://profimize.com,https://www.profimize.com
DB_NAME=cpaneluser_profimize
DB_USER=cpaneluser_dbuser
DB_PASSWORD=<your-db-password>
```

---

## Step 5 — Install Dependencies

In cPanel **Terminal** (or SSH):
```bash
# Copy the virtualenv activation command from the Setup Python App page, then:
source /home/cpaneluser/virtualenv/profimize/3.11/bin/activate

# Navigate to app root
cd ~/profimize

# Install packages
pip install -r requirements.txt
```

---

## Step 6 — Migrate, Collect Static, Create Superuser

```bash
# Still in the activated virtualenv:
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

The `migrate` command runs the seed migration automatically, populating:
- SiteSettings (brand info, contact details)
- Services (6 services)
- Projects (6 portfolio items)
- Testimonials (3 client quotes)
- Stats (4 key metrics)

---

## Step 7 — Restart the App

- cPanel → **Setup Python App** → click **Restart** next to your app
- Or via terminal: `touch ~/profimize/tmp/restart.txt`

---

## Step 8 — Verify

1. Visit `https://profimize.com` — site should load
2. Visit `/admin/` — log in with your superuser credentials (Jazzmin theme)
3. Create a blog post with an **image thumbnail** → verify it appears
4. Create a blog post with a **YouTube URL** → click the play overlay → lightbox opens, video plays
5. Check `/sitemap.xml` — all static pages + blog posts listed
6. Check `/robots.txt`
7. Use [opengraph.xyz](https://www.opengraph.xyz) or Facebook Sharing Debugger to verify OG tags
8. Run Lighthouse mobile audit (target: 95+ on all metrics)

---

## Day-to-Day Operations

### After any code change:
```bash
source /home/cpaneluser/virtualenv/profimize/3.11/bin/activate
cd ~/profimize
python manage.py collectstatic --noinput   # if CSS/JS/images changed
touch tmp/restart.txt                       # restart Passenger
```

### Create / publish a blog post:
1. `/admin/` → Blog → Posts → Add Post
2. Fill in title, excerpt, body (CKEditor), category, tags, author
3. Add an **image thumbnail** OR a **YouTube URL** (not both required)
4. Set status to **Published** → Save
5. Post appears at `/blog/<slug>/`

---

## Common cPanel Gotchas

| Issue | Fix |
|---|---|
| `500 Internal Server Error` | Check `DEBUG=False` + correct `ALLOWED_HOSTS` |
| Static files 404 | Run `collectstatic`, check WhiteNoise is in MIDDLEWARE above session |
| MySQL auth error | Verify PyMySQL `install_as_MySQLdb()` in `config/__init__.py` |
| Passenger not starting | Check `passenger_wsgi.py` path; confirm virtualenv is activated |
| Media files not serving | Django serves media in DEBUG mode. In prod, configure an Alias or serve via public folder |
| Images not compressing | Pillow failure is silent; site keeps running; check server logs |

---

## Media Files in Production

WhiteNoise only serves `/static/`. For `/media/` (user-uploaded images):

**Option A** — Create a symlink:
```bash
ln -s ~/profimize/media ~/public_html/media
```
Then Apache serves `/media/` directly.

**Option B** — Add to `.htaccess` in `public_html`:
```apache
Alias /media/ /home/cpaneluser/profimize/media/
```

---

## Optional: Enable Email Notifications for Contact Form

In `apps/pages/views.py`, locate the `ContactMessage.objects.create(...)` lines and add after:

```python
# Uncomment and configure to enable email alerts for new contact messages
# from django.core.mail import send_mail
# send_mail(
#     subject=f"New Profimize enquiry: {cd['subject']}",
#     message=f"From: {cd['name']} <{cd['email']}>\n\n{cd['message']}",
#     from_email=settings.DEFAULT_FROM_EMAIL,
#     recipient_list=["souravmondalcode@gmail.com"],
#     fail_silently=True,
# )
```

And add to `settings.py`:
```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.profimize.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = "Profimize <noreply@profimize.com>"
```
