# 📱 Medical Telegram Bot

Telegram bot interface for the Medical App using aiogram framework.

## 🚀 Features

- 👨⚕️ **View Doctors** - Browse available doctors and specializations
- 📅 **View Appointments** - Check appointment schedules
- 🔐 **Authentication** - Secure login with medical app credentials
- 💬 **Interactive Interface** - User-friendly inline keyboards
- 🔄 **Real-time Data** - Direct integration with FastAPI backend

## 🛠️ Tech Stack

- **aiogram 3.3.0** - Modern Telegram Bot framework
- **aiohttp** - Async HTTP client for API calls
- **python-dotenv** - Environment variables management

## ⚙️ Setup

### 1. Create Telegram Bot

1. Find [@BotFather](https://t.me/botfather) in Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token

### 2. Configure Environment

```bash
cd med-bot
cp .env.example .env
```

Edit `.env` file:
```env
BOT_TOKEN=your_bot_token_here
API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python bot.py
```

## 📱 Usage

1. **Start the bot** - Send `/start` command
2. **Login** - Click "🔐 Войти" and send credentials in format: `email password`
3. **Browse data** - Use "👨⚕️ Врачи" and "📅 Записи" buttons

### Example Login
```
admin@example.com admin123
```

## 🏗️ Architecture

```
Telegram Bot ←→ API Client ←→ FastAPI Backend ←→ Database
     ↑              ↑              ↑              ↑
  aiogram      aiohttp        FastAPI      PostgreSQL
```

## 📁 Project Structure

```
med-bot/
├── bot.py              # Main bot application
├── api_client.py       # HTTP client for FastAPI
├── requirements.txt    # Dependencies
├── .env               # Environment variables
└── README.md          # This file
```

## 🔐 Security

- JWT token authentication
- Secure credential handling
- Session state management
- Input validation

## 🚀 Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

### Environment Variables

- `BOT_TOKEN` - Telegram bot token from @BotFather
- `API_BASE_URL` - Medical app API base URL

## 🤝 Integration

The bot integrates with the main Medical App through REST API:

- **Authentication**: `POST /auth/login`
- **Doctors**: `GET /doctors`
- **Appointments**: `GET /appointments`

## 📝 License

This project is part of the Medical App and follows the same MIT License.