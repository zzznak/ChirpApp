# ChirpApp - Messenger like Augramm

Красивый мессенджер в стиле Augramm/Telegram с поддержкой шифрования, групп и личных чатов.

## 🎨 Особенности

- 🔒 End-to-End шифрование сообщений
- 💬 Личные чаты и группы
- 👥 Список контактов с поиском
- 🌙 Тёмная тема (как Augramm)
- ⚡ WebSocket для реального времени
- 📱 Красивый интерфейс Flet
- 📊 История сообщений в БД

## 📋 Требования

```bash
pip install flet websockets fastapi uvicorn cryptography
```

## 🚀 Запуск

### 1. Инициализация БД
```bash
python database.py
```

### 2. Запуск сервера (в отдельном терминале)
```bash
python backend.py
```

### 3. Запуск клиента
```bash
python main.py
```

## 📁 Структура проекта

```
ChirpApp/
├── main.py              # Главный UI клиента
├── backend.py           # WebSocket сервер (FastAPI)
├── database.py          # SQLite база данных
├── security.py          # Шифрование (Fernet)
├── views.py             # UI компоненты
├── models.py            # Модели данных
└── README.md
```

## 🔐 Безопасность

Все сообщения шифруются с помощью Fernet (симметричное шифрование). Пароли хранятся в виде SHA-256 хешей.

## 👨‍💻 Автор

zzznak

## 📄 Лицензия

MIT