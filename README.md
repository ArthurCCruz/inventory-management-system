# Inventory Management System

A full-stack inventory management system built with Django REST Framework (backend) and React (frontend), fully containerized with Docker for both development and production environments.

## 🏗️ Architecture

This project consists of two independent applications:

- **Backend** (`/backend`): Django 4.2 + Django REST Framework + PostgreSQL
- **Frontend** (`/frontend`): React + Vite + TanStack Query + Mantine + Tailwind CSS

Each application has its own Dockerfile and docker-compose.yml for independent development and deployment.

## 📦 Tech Stack

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
