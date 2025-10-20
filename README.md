### Hexlet tests and linter status:
[![Actions Status](https://github.com/YurasovAleksey/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/YurasovAleksey/python-project-52/actions)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=YurasovAleksey_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=YurasovAleksey_python-project-52)

[![Python CI](https://github.com/YurasovAleksey/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/YurasovAleksey/python-project-52/actions/workflows/pyci.yml)

# Task Manager

Веб-приложение для управления задачами, разработанное на Django. Позволяет создавать, назначать и отслеживать задачи с системой статусов и меток.

##  Функциональность

- **Управление пользователями**: Регистрация, аутентификация, CRUD операции
- **Управление задачами**: Создание, редактирование, удаление задач
- **Система статусов**: Настройка статусов выполнения задач
- **Метки (теги)**: Гибкая система категоризации задач
- **Фильтрация**: Поиск задач по статусу, исполнителю, меткам
- **Авторизация**: Разграничение прав доступа

##  Технологии

- **Backend**: Django 5.2, Python 3.13
- **Database**: PostgreSQL
- **Testing**: pytest, pytest-django
- **Code Quality**: flake8, coverage
- **CI/CD**: GitHub Actions, SonarQube

##  Установка и запуск

### Предварительные требования
- Python 3.13+
- PostgreSQL
- uv (менеджер зависимостей)

### Установка

1. Клонируйте репозиторий:
git clone <repository-url>
cd python-project-52
2. Установите зависимости:
make install
Настройте базу данных в task_manager/settings.py

3. Примените миграции:
make migrate

4. Запустите сервер:
make run
Приложение будет доступно по адресу: http://localhost:8000

Доступные команды:
make install - установка зависимостей

make migrate - применение миграций

make start - запуск сервера разработки

make test - запуск тестов

make lint - проверка стиля кода

make test-coverage - тесты с отчетом покрытия

👥 Разработчики:
Алексей Юрасов

Ссылка на проект на Render: https://python-project-52-1-wmx3.onrender.com
