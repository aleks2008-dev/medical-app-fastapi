# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Запуск
docker-compose up --build

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
uvicorn app.main:app --reload

# Запуск тестов
docker exec -it medical_app bash
pytest