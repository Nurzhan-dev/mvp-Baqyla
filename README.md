# Baqyla CRM

Baqyla — это минимальная CRM-система для внутреннего контроля поручений в государственных учреждениях. Руководитель создаёт поручения, прикрепляет документы, а сотрудники получают и просматривают их.

## 🚀 Возможности

- Авторизация по ролям: руководитель и сотрудник
- Загрузка и просмотр документов
- Статусы задач: новое, срочно, просрочено
- Многоязычность: русский и казахский интерфейс
- Сессии и защита доступа

## 📦 Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Nurzhan-dev/baqyla-crm.git
cd baqyla-crm
pip install -r requirements.txt
python app.py
http://localhost:5000
baqyla-crm/
├── app.py                # Основной Flask-приложение
├── requirements.txt      # Зависимости
├── templates/            # HTML-шаблоны (Jinja2)
│   ├── login.html
│   └── index.html
├── static/
│   └── logo.png          # Логотип
└── uploads/              # Загруженные документы
Автор
Nurzhan-dev
GitHub: @Nurzhan-dev
