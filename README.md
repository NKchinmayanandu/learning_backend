# 🍽️ Restaurant Listing API

A REST API for a restaurant listing platform built with **FastAPI** and **PostgreSQL**. Supports JWT-authenticated owner and user roles, structured CRUD for restaurants and menu items, Redis caching, and is fully containerized with Docker.

---

## Features

- **JWT Authentication** — Signup/login with role-based access (`owner` / `user`)
- **Restaurant CRUD** — Owners can create, update, and delete their restaurants
- **Menu Management** — Owners can add food items to their restaurants
- **Redis Caching** — Frequently accessed restaurant listings are cached to reduce database reads
- **Services Layer** — Business logic is separated from route handlers
- **Alembic Migrations** — Schema versioning via Alembic
- **Dockerized** — App + PostgreSQL + Redis run via Docker Compose

---

## Tech Stack

| Layer        | Technology                     |
|--------------|-------------------------------|
| Framework    | FastAPI                       |
| Database     | PostgreSQL (via SQLAlchemy)   |
| Cache        | Redis                         |
| Auth         | JWT (`python-jose` + `passlib`) |
| Migrations   | Alembic                       |
| Validation   | Pydantic v2                   |
| Container    | Docker + Docker Compose       |

---

## Project Structure

```
.
├── main.py                     # App entry point
├── apps/
│   ├── models.py               # SQLAlchemy models (User, Restaurant, Food)
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── database.py             # DB session + engine setup
│   ├── redis.py                # Redis client setup
│   ├── config.py               # Environment config
│   ├── routers/
│   │   ├── auth.py             # /auth endpoints (signup, login)
│   │   └── restaurants.py      # /restaurant endpoints (CRUD, food, search)
│   ├── services/
│   │   ├── auth_services.py    # Authentication business logic
│   │   ├── restaurant_services.py  # Restaurant + cache logic
│   │   └── user_services.py    # User lookup logic
│   └── utils/
│       ├── deps.py             # JWT dependency injection
│       ├── jwt.py              # Token creation/decoding
│       ├── security.py         # Password hashing/verification
│       └── cache.py            # Redis get/set helpers
├── migrations/                 # Alembic migration files
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## API Endpoints

### Auth — `/auth`

| Method | Endpoint        | Description              | Auth |
|--------|-----------------|--------------------------|------|
| POST   | `/auth/signup`  | Register a new user      | ❌   |
| POST   | `/auth/login`   | Login and get JWT token  | ❌   |

### Restaurants — `/restaurant`

| Method | Endpoint              | Description                        | Auth     |
|--------|-----------------------|------------------------------------|----------|
| GET    | `/restaurant/`        | List all restaurants (paginated)   | ❌       |
| GET    | `/restaurant/{id}`    | Get restaurant by ID               | ❌       |
| POST   | `/restaurant/`        | Create a restaurant                | ✅ owner |
| PATCH  | `/restaurant/{id}`    | Update restaurant name             | ✅ owner |
| DELETE | `/restaurant/{id}`    | Delete a restaurant                | ✅ owner |
| POST   | `/restaurant/foods`   | Add a food item to a restaurant    | ✅ owner |
| GET    | `/restaurant/food`    | Find restaurants by food name      | ❌       |

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose

### 1. Clone the repo

```bash
git clone https://github.com/NKchinmayanandu/learning_backend.git
cd learning_backend
```

### 2. Configure environment

Create a `.env` file in the root (or update `docker-compose.yml` directly):

```env
DATABASE_URL=postgresql://chinmay:yourpassword@db:5432/restaurant_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

The API will be live at **http://localhost:8000**

### 4. Run database migrations

```bash
docker-compose exec app alembic upgrade head
```

### 5. Explore the API docs

FastAPI auto-generates interactive docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Running Locally (without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
```

> Ensure PostgreSQL and Redis are running and your `.env` is set up correctly.

---

## Role-Based Access

When signing up, set the `role` field to either `"user"` or `"owner"`:

```json
{
  "email": "owner@example.com",
  "password": "securepassword",
  "role": "owner"
}
```

Only users with the `owner` role can create, update, or delete restaurants and add food items.
