# 1. Базовий образ
FROM python:3.11-slim
# 2.Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*
# 3. Робоча директорія в контейнері
WORKDIR /app

# 4. Копіюємо файли у контейнер
COPY . .

# 5. Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# 6. Вказуємо порт
EXPOSE 8501

# 7. Команда запуску Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
