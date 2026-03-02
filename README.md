# Inventory Management System

A full-stack inventory management system built with Django REST Framework (backend) and React (frontend), fully containerized with Docker for both development and production environments.

## 🏗️ Architecture

This project consists of two independent applications:

- **Backend** (`/backend`): Django 4.2 + Django REST Framework + PostgreSQL
- **Frontend** (`/frontend`): React + Vite + TanStack Query + Mantine + Tailwind CSS

Each application has its own Dockerfile and docker-compose.yml for independent development and deployment.

## 📦 Tech Stack

### Backend
- Python 3.11
- Django 4.2 LTS
- Django REST Framework
- PostgreSQL 15

### Frontend
- Node.js 20
- React 18
- Vite 5
- TanStack Query (data fetching)
- Mantine 7 (UI components)
- Tailwind CSS 3 (styling)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (optional, for cloning)

### Development Setup

#### Backend Development

1. Navigate to the backend directory:
```bash
cd backend
```

2. Copy the environment file and configure if needed:
```bash
cp .env.example .env
```

3. Start the backend services (Django + PostgreSQL):
```bash
docker compose up --build
```

The backend API will be available at:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Health check: http://localhost:8000/api/health/

**Hot Reload**: The Django development server will automatically reload when you edit Python files in the `backend/` directory.

##### Running Tests

To run tests for the backend:

```bash
# Run all tests
docker compose exec web python manage.py test

# Run specific app tests
docker compose exec web python manage.py test apps.products
docker compose exec web python manage.py test apps.auth

# Run specific test file
docker compose exec web python manage.py test apps.products.tests.test_models

# Run specific test class
docker compose exec web python manage.py test apps.products.tests.test_models.ProductModelTestCase

# Run specific test method
docker compose exec web python manage.py test apps.products.tests.test_models.ProductModelTestCase.test_valid_product_creation

# Run in parallel (faster)
docker compose exec web python manage.py test --parallel

# Keep database between runs (faster for iterative testing)
docker compose exec web python manage.py test --keepdb

# Run with verbose output
docker compose exec web python manage.py test --verbosity=2
```

#### Frontend Development

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Copy the environment file and configure if needed:
```bash
cp .env.example .env
```

3. Start the frontend service (Vite dev server):
```bash
docker compose up --build
```

The frontend will be available at:
- Frontend: http://localhost:5173/

**Hot Module Replacement (HMR)**: Vite will automatically reload when you edit files in the `frontend/src/` directory.

## 🔧 Configuration

### Backend Environment Variables

Edit `backend/.env`:

```bash
# Django settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=inventory_db
DB_USER=inventory_user
DB_PASSWORD=inventory_password
DB_HOST=db
DB_PORT=5432

# Superuser data
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com

### Frontend Environment Variables

Edit `frontend/.env`:

```bash
# API endpoint for backend
VITE_API_URL=http://localhost:8000
```

## 📝 Common Development Tasks

### Frontend

**Install new npm package:**
```bash
# Stop the container first, then:
cd frontend
npm install <package-name>
# Update package.json, then rebuild:
docker compose up --build
```

### Backend

**Run Django management commands:**
```bash
# Access the container
docker compose exec web bash

# Inside the container:
python manage.py migrate
python manage.py createsuperuser
python manage.py makemigrations
python manage.py shell
```

**Database access:**
```bash
docker compose exec db psql -U inventory_user -d inventory_db
```