
 Social Media API (Django)

This repository contains my Capstone Project: **Social Media API** built with Django and Django REST Framework.  
The goal is to design and build a backend API for a social media platform where users can interact by creating posts, commenting, and engaging with other users.
 🚀 Features (Planned)
- User registration & authentication
- User profiles
- Posts (CRUD)
- Comments on posts
- Likes / reactions
- Follow system
- Search functionality

# Social Media API

A Django + DRF backend that supports posts, likes, following, feed, bookmarks, trending, and JWT auth.

## Demo (Loom)
_Add your Loom link here._

## Features
- Posts CRUD (author-only edits/deletes)
- Likes (idempotent like/unlike, list who liked)
- Follow/Unfollow and Feed (followed users + your own posts)
- Bookmarks (save/unsave, list my saved posts)
- Trending posts (most liked in the last N days)
- JWT Authentication (access/refresh)

## Quickstart (Local)
```bash
git clone https://github.com/Abby966/social_media_API.git
cd social_media_API
python -m venv .venv         # or: py -m venv .venv (Windows)
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API root: http://127.0.0.1:8000/api/

## Auth
- `POST /api/token/` → obtain access & refresh
- `POST /api/token/refresh/` → refresh access

## Key Endpoints
- `GET/POST /api/posts/` — list/create posts
- `GET /api/posts/{id}/` — retrieve post
- `POST /api/posts/{id}/like/` — like
- `DELETE /api/posts/{id}/unlike/` — unlike
- `GET /api/posts/{id}/likes/` — who liked
- `GET /api/feed/` — my feed (followed + own)
- `POST /api/follow/` — follow (`{"following": <user_id>}`)
- `GET /api/follow/` — list my follows
- `GET /api/follow/suggested/` — who to follow
- `POST /api/posts/{id}/bookmark/` — save a post
- `DELETE /api/posts/{id}/unbookmark/` — unsave
- `GET /api/posts/bookmarks/` — my saved posts
- `GET /api/posts/trending/?days=7&min_likes=1` — trending

## Postman
Import the collection: **social_media_api_postman.json**

1. `Auth - Obtain Token` → copy `access`
2. For protected requests, set header: `Authorization: Bearer <ACCESS>`

## Tech
- Django 5 + Django REST Framework
- SimpleJWT
- SQLite (dev)
- Python 2025-09-07

## Notes
- Default DRF pagination (10/page)
- Trailing slash on endpoints (e.g. `/api/posts/`)
