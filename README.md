# AI Fitness Ecosystem 🏋️‍♂️🤖

A production-ready, AI-powered fitness tracking platform built with **Next.js 15**, **FastAPI**, **MySQL**, and **AI/ML** services.

![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)

## ✨ Features

- 📊 **Real-time Dashboard** — Steps, calories, water, BMI, workout tracking
- 🍽️ **Nutrition Tracker** — 85+ Indian & international foods, meal logging, macro tracking
- 💪 **Workout Engine** — 38+ exercises, session logging, workout plans, stats
- 🤖 **AI Food Scanner** — Upload food photos → AI nutrition analysis
- 🧠 **AI Coach** — Context-aware fitness coaching chatbot
- 📈 **Analytics** — Weekly/monthly trends, fitness score, weight progress
- 🏆 **Achievements** — 12 unlockable badges with XP system
- 📱 **Device Sync** — Bluetooth device integration
- 🔐 **JWT Auth** — Register, login, refresh tokens, admin roles
- 🎵 **Music Integration** — Spotify/YouTube workout playlists

## 🏗️ Architecture

```
Frontend (Next.js 15)  →  API Gateway (FastAPI)  →  MySQL 8.0
     ↓                         ↓                       ↓
  Redux Store            Service Layer           Repository Layer
     ↓                         ↓                       ↓
  19 Pages              8 Business Services      10 Data Repos
                               ↓
                        AI Services (OpenAI/Gemini)
                               ↓
                        Celery Workers (Redis)
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ & npm
- Python 3.12+
- MySQL 8.0+
- Redis (optional, for background tasks)

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-fitness-ecosystem.git
cd ai-fitness-ecosystem
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials

# Seed database (creates tables + demo data)
python -m scripts.seed

# Start server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### 4. Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

### Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@aifitness.com | Admin@1234 |
| User | demo@aifitness.com | Demo@1234 |

## 🐳 Docker

```bash
docker-compose up -d
# Starts MySQL, Redis, Backend, and Frontend
```

## 📁 Project Structure

```
ai-fitness-ecosystem/
├── backend/
│   ├── app/
│   │   ├── ai/              # AI vision + coach services
│   │   ├── api/endpoints/   # 11 API route files
│   │   ├── core/            # Config, security, middleware, exceptions
│   │   ├── db/              # SQLAlchemy engine + session
│   │   ├── models/          # 8 model files (30+ tables)
│   │   ├── repositories/    # 10 data access repos
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # 10 business logic services
│   │   └── utils/           # Calculations, validators, pagination
│   ├── alembic/             # Database migrations
│   ├── scripts/             # Seed script (85+ foods, 38+ exercises)
│   ├── tests/               # Pytest test suite (26 tests)
│   └── workers/             # Celery background tasks
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js 15 App Router (19 pages)
│   │   ├── components/      # Reusable UI components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── lib/             # API client + utilities
│   │   └── store/           # Redux Toolkit state management
│   └── public/
├── database/                # SQL schema + seed scripts
├── nginx/                   # Reverse proxy config
└── docker-compose.yml       # Full stack orchestration
```

## 🔑 API Endpoints (40+)

| Module | Endpoints | Description |
|--------|-----------|-------------|
| Auth | 6 | Register, login, refresh, profile |
| Dashboard | 1 | Aggregated fitness summary |
| Steps | 5 | Log, today, week, month, statistics |
| Nutrition | 8 | Meals, foods, water tracking |
| Workouts | 7 | Sessions, exercises, plans, stats |
| Goals | 4 | BMI, weight progress, achievements |
| Analytics | 5 | Daily/weekly/monthly, fitness score |
| AI | 2 | Food scanner, AI coach |
| Notifications | 3 | List, mark read |
| Devices | 4 | Register, sync, remove |
| Admin | 3 | System stats, user management |

## 🧪 Testing

```bash
cd backend
python -m pytest tests/ -v
# 26 tests, all passing
```

## 📊 Seed Data

The seed script populates the database with:
- **85+ foods** (Indian & international with full nutrition data)
- **38+ exercises** (strength, cardio, HIIT, flexibility)
- **12 achievements** with XP rewards
- **90 days** of demo fitness history
- **2 users** (admin + demo with full profiles)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, TypeScript, Redux Toolkit, Framer Motion, Recharts, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic |
| Database | MySQL 8.0, Redis 7 |
| AI/ML | OpenAI GPT-4o, Google Gemini, Pillow |
| Workers | Celery with Redis broker |
| Auth | JWT (access + refresh tokens), bcrypt |
| Testing | Pytest, pytest-asyncio |
| Deploy | Docker, Railway, Nginx |

## 📄 License

MIT License — free to use and modify.

---

Built with ❤️ by Dhruv Vijay
