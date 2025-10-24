# Online Courses Platform (учебный проект)

Простой проект на Django — онлайн-платформа для курсов и лекций.

## Быстрый старт (локально)

1. Клонировать репозиторий:
```bash
git clone https://github.com/ВАШ_ЛОГИН/online-courses-platform.git
cd online-courses-platform
```

2. Создать виртуальное окружение и активировать:

    Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

    Windows:

```bash
python -m venv venv
venv\Scripts\activate.bat
```

3. Установить зависимости:

```bash

pip install -r requirements.txt
```

4. Выполнить миграции и запустить сервер:


```bash

python manage.py migrate
python manage.py runserver
```

5. Открыть в браузере: http://127.0.0.1:8000/


# Что реализовано
Список курсов (данные в коде).

Страница курса + форма записи (форма не сохраняет в БД — имитация).

Настройки темы и языка, сохранённые в cookies.

Сохранение последних посещённых страниц в cookie last_visited.

Как изменить данные курсов
Откройте courses/views.py и отредактируйте список COURSES.

# Команды git
```bash

git add .
git commit -m "Описание изменений"
git push
```