# 🏥 Medical App - FastAPI Clean Architecture

> Enterprise-level medical management system built with Clean Architecture principles

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io)
[![Tests](https://img.shields.io/badge/Tests-65%20passing-brightgreen.svg)](#testing)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange.svg)](#architecture)

## 🎯 Project Overview

A comprehensive medical management system demonstrating **Clean Architecture** principles with complete separation of concerns, dependency inversion, and enterprise-level patterns.

### Key Features
- 👨‍⚕️ **Doctor Management** - CRUD operations with role-based access
- 👤 **User Management** - Registration, authentication, profile management  
- 📅 **Appointment System** - Booking and scheduling functionality
- 🏥 **Room Management** - Medical facility room allocation
- 🔐 **JWT Authentication** - Secure token-based auth with refresh tokens
- 📊 **Role-Based Access Control** - Admin, Doctor, User roles
- 🔄 **Password Reset** - Email-based password recovery
- 📱 **Telegram Bot** - Alternative interface using aiogram

## 🏗️ Architecture

### Clean Architecture Layers
```
┌─────────────────────────────────────────┐
│              API Layer                  │ ← HTTP handlers, routing
├─────────────────────────────────────────┤
│           Infrastructure                │ ← Database, Redis, Email
├─────────────────────────────────────────┤
│             Adapters                    │ ← Repository implementations
├─────────────────────────────────────────┤
│            Use Cases                    │ ← Business logic
├─────────────────────────────────────────┤
│             Domain                      │ ← Entities, Interfaces
└─────────────────────────────────────────┘
```

### SOLID Principles Implementation
- ✅ **Single Responsibility** - Each class has one reason to change
- ✅ **Open/Closed** - Open for extension, closed for modification
- ✅ **Liskov Substitution** - Implementations are interchangeable
- ✅ **Interface Segregation** - Focused, specific interfaces
- ✅ **Dependency Inversion** - Depend on abstractions, not concretions

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Async ORM with PostgreSQL
- **Pydantic** - Data validation and serialization
- **JWT** - Secure authentication
- **Redis** - Session management and caching

### Database
- **PostgreSQL** - Primary database
- **Redis** - Token storage and sessions

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Pytest** - Comprehensive testing suite

### Additional
- **Aiogram** - Telegram bot framework
- **Passlib** - Password hashing
- **Python-Jose** - JWT handling

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aleks2008-dev/medical-app-fastapi.git
   cd medical-app-fastapi
   ```

2. **Start with Docker**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Manual Setup (Development)

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📱 Telegram Bot

The project includes a Telegram bot for alternative access built with **aiogram 3.3.0**:

### Features
- 👨⚕️ Browse doctors and specializations
- 📅 View appointment schedules  
- 🔐 Secure authentication with medical app
- 💬 Interactive inline keyboards
- 🔄 Real-time data integration

### Quick Setup

1. **Get bot token from [@BotFather](https://t.me/botfather)**
2. **Configure environment**
   ```bash
   cd med-bot
   cp .env.example .env
   # Edit .env with your bot token
   ```
3. **Install and run**
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```

📖 **[Full Bot Documentation](med-bot/README.md)**

## 🧪 Testing

Comprehensive test suite with **65 tests** covering all layers:

```bash
# Run all tests
docker exec medical_app pytest -v

# Run with coverage
docker exec medical_app pytest --cov=app --cov-report=html
```

### Test Coverage
- ✅ **Unit Tests** - Domain entities and use cases
- ✅ **Integration Tests** - Repository implementations
- ✅ **API Tests** - HTTP endpoints
- ✅ **Authentication Tests** - Security flows

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/reset-password` - Password reset

### Users
- `GET /api/v1/users` - List users (Admin only)
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user
- `PATCH /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Doctors
- `GET /api/v1/doctors` - List doctors
- `POST /api/v1/doctors` - Create doctor (Admin only)
- `GET /api/v1/doctors/{id}` - Get doctor
- `PATCH /api/v1/doctors/{id}` - Update doctor (Admin only)
- `DELETE /api/v1/doctors/{id}` - Delete doctor (Admin only)

### Appointments
- `GET /api/v1/appointments` - List appointments
- `POST /api/v1/appointments` - Create appointment
- `GET /api/v1/appointments/{id}` - Get appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

### Rooms
- `GET /api/v1/rooms` - List rooms
- `POST /api/v1/rooms` - Create room

## 🔐 Security Features

- **JWT Authentication** with access/refresh tokens
- **Role-based authorization** (Admin, Doctor, User)
- **Password hashing** with SHA256
- **Token blacklisting** in Redis
- **Session management**
- **Input validation** with Pydantic
- **SQL injection protection** via ORM

## 📁 Project Structure

```
app/
├── domain/                 # Business entities and interfaces
│   ├── entities/          # Core business objects
│   └── interfaces/        # Abstract interfaces
├── use_cases/             # Business logic layer
├── repository/            # Data access interfaces
├── adapters/              # Repository implementations
├── infrastructure/        # External services (DB, Redis)
├── api/                   # HTTP layer
│   └── routers/          # FastAPI routers
├── core/                  # Cross-cutting concerns
└── tests/                 # Test suite
```

## 🎨 Design Patterns Used

- **Repository Pattern** - Data access abstraction
- **Use Case Pattern** - Business logic encapsulation
- **Dependency Injection** - Loose coupling
- **Factory Pattern** - Object creation
- **Strategy Pattern** - Algorithm selection
- **Adapter Pattern** - Interface adaptation
- **Command Pattern** - Request encapsulation

## 🚀 Deployment

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
```env
DATABASE_URL=postgresql://user:pass@localhost/medical_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Aleks** - [GitHub Profile](https://github.com/aleks2008-dev)

---

⭐ **Star this repository if you found it helpful!**

## 📈 Project Highlights

- 🏆 **Clean Architecture 10/10** - Perfect separation of concerns
- 🧪 **65 Tests Passing** - Comprehensive test coverage
- 🔒 **Enterprise Security** - JWT, RBAC, password hashing
- 🐳 **Docker Ready** - Full containerization
- 📱 **Multi-Interface** - REST API + Telegram Bot
- 🎯 **SOLID Principles** - Professional code quality
- 📊 **Production Ready** - Logging, health checks, graceful shutdown