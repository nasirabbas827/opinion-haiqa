# opinion_haiqa_final  

A lightweight Django web‑application that lets users create posts, comment on them, and automatically evaluates comment sentiment. The project is structured as a reusable Django app (`myapp`) and includes ready‑to‑run migrations, admin configuration, and basic media handling.

---

## Overview  

`opinion_haiqa_final` demonstrates a full‑stack Python/Django solution for a simple opinion‑sharing platform:

* **Posts** – users can publish textual posts.  
* **Comments** – each post can receive multiple comments.  
* **Sentiment analysis** – every comment is automatically labelled with a sentiment (positive/negative/neutral) and a confidence score.  
* **Media** – profile picture placeholders are stored under `media/profile_pics/`.  

The repository contains a standard Django project layout with a single reusable app (`myapp`). All database schema changes are captured in the migration files.

---

## Features  

| Feature | Description |
|---------|-------------|
| **User‑generated content** | Create, edit, and delete posts and comments via the Django admin or custom views. |
| **Automatic sentiment labeling** | On comment save, a sentiment label (`positive`, `negative`, `neutral`) and a numeric score are stored (`sentiment_label`, `sentiment_score`). |
| **Admin interface** | Full CRUD access for posts, comments, and users through Django’s built‑in admin. |
| **Media handling** | Default profile pictures (`DB.png`, `day.png`) are served from the `media/profile_pics/` directory. |
| **Test suite** | Basic unit tests located in `myapp/tests.py`. |
| **Reusable app** | `myapp` can be plugged into any Django project by adding it to `INSTALLED_APPS`. |

---

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.9+ |
| **Web framework** | Django 4.x |
| **Database** | SQLite (default) – can be swapped for PostgreSQL, MySQL, etc. |
| **Sentiment analysis** | Placeholder – integrate any NLP library (e.g., TextBlob, spaCy, HuggingFace). |
| **Front‑end** | Django templates (HTML/CSS) – extend as needed. |
| **Version control** | Git (GitHub) |

---

## Installation  

> **Prerequisite:** Ensure you have Python 3.9 or newer and `git` installed.

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/opinion_haiqa_final.git
cd opinion_haiqa_final

# 2. Create and activate a virtual environment
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt   # (create this file if not present, e.g. Django==4.*)

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser for admin access
python manage.py createsuperuser
```

> **Optional:** If you want to use a different database, edit `op