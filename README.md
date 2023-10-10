Для налаштування сервісу повинні бути прописані такі змінні середовища: 
SQLALCHEMY_DATABASE_URL
JWT_SECRET_KEY
JWT_ALGORITHM
cloud_name
cloud_api_key
cloud_api_secret
OPENAI_API_KEY
Команда для запуску: uvicorn main:app --host localhost --port 8080 --reload
Віртуальне оточення: poetry. Запускати командою poetry shell в корені проекту. 