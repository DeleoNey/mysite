# Django Blog Project

A blog web application built with **Django 5** and **Bootstrap 5**. Users can register, create and edit posts, add comments, and like posts.

---

## Features

* User registration and authentication
* User profile with avatar
* CRUD (Create, Read, Update, Delete) for posts
* Likes for posts (ManyToManyField)
* Comments for posts
* Search posts by title
* Automatic slug generation for posts and profiles (supports Ukrainian characters)
* Access control: only authors can edit or delete their posts

---

## Technology Stack

* Python 3.13
* Django 5.2.6
* SQLite (default, can switch to PostgreSQL)
* Bootstrap 5
* Pytils (for slug transliteration)

---

## Installation

1. Clone the repository:

```bash
git clone <REPO_URL>
cd mysite
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Open in browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Endpoints

### Posts

| Method    | URL                    | Description                       |
| --------- | ---------------------- | --------------------------------- |
| GET       | `/`                    | List all posts                    |
| GET       | `/post/<slug>/`        | View post details                 |
| GET, POST | `/post/new/`           | Create a new post (auth required) |
| GET, POST | `/post/<slug>/edit/`   | Edit post (author only)           |
| POST      | `/post/<slug>/delete/` | Delete post (author only)         |

### Users

| Method    | URL                    | Description                       |
| --------- | ---------------------- | --------------------------------- |
| GET, POST | `/users/register/`     | User registration                 |
| GET       | `/users/profile/`      | View user profile (auth required) |
| GET, POST | `/users/profile/edit/` | Edit user profile (auth required) |
| GET, POST | `/users/login/`        | Login                             |
| GET       | `/users/logout/`       | Logout                            |

---

## Models

**Post**

* `title` – Post title
* `content` – Post content
* `author` – ForeignKey to User
* `image` – Optional image
* `slug` – Auto-generated unique slug
* `likes` – Users who liked the post

**Comment**

* `post` – ForeignKey to Post
* `author` – User who commented
* `content` – Text of comment

**Profile**

* `user` – OneToOneField to User
* `name` – Display name
* `slug` – Slug for profile URL
* `avatar` – Profile picture

---

## Usage

* Create, edit, delete posts as an authenticated user
* Like/unlike posts in post detail view
* Add comments to posts
* Search posts by title using the search form

---

## Tests

Run tests for the main app:

```bash
python manage.py test main
```

Run tests for users app:

```bash
python manage.py test users
```

Tests cover:

* Post creation and update
* Like functionality
* Comment creation
* User profile creation and update

---

## Slug handling

* Ukrainian characters are transliterated to English using `pytils.translit`
* Ensures uniqueness with a counter if the same slug already exists



Do you want me to do that?
