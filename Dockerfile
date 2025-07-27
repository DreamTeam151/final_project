# 1. Базовий образ
FROM python:3.11-slim

# 2. Робоча директорія в контейнері
WORKDIR /app

# 3. Копіюємо файли у контейнер
COPY . .

# 4. Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# 5. Вказуємо порт
EXPOSE 8501

# 6. Команда запуску Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
