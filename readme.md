# TeamFinder

TeamFinder — веб-приложение на Django для поиска единомышленников и совместной работы над Pet-проектами. Пользователи могут создавать профиль, публиковать проекты, присоединяться к чужим проектам и просматривать других участников платформы.

## Возможности проекта

- регистрация и авторизация по email и паролю;
- просмотр списка проектов с пагинацией;
- просмотр списка пользователей с пагинацией;
- создание и редактирование профиля;
- создание и редактирование проектов;
- завершение проекта владельцем;
- участие в чужих проектах;
- автогенерация аватара при регистрации (первая буква имени на цветном фоне);
- смена пароля.

## Вариант 1: Избранное и фильтрация пользователей

Авторизованный пользователь может добавлять проекты в избранное:

- кнопка «Добавить в избранное» (иконка сердечка) доступна на главной странице и на странице проекта;
- страница `/projects/favorites/` показывает только избранные проекты текущего пользователя;
- повторный клик по сердечку убирает проект из избранного.

На странице списка пользователей `/users/list/` доступна фильтрация по 4 критериям (только для авторизованных):

- **Авторы избранных проектов** — пользователи, чьи проекты добавлены в избранное;
- **Авторы проектов, в которых я участвую** — владельцы проектов с текущим пользователем в составе;
- **Пользователи, которым нравятся мои проекты** — те, кто добавил мои проекты в избранное;
- **Участники моих проектов** — все участники проектов, где я владелец.

Активный фильтр подсвечивается, рядом появляется кнопка «Сбросить».

## Запуск проекта

**Требования:** Python 3.11+, Docker и Docker Compose

### 1. Клонировать репозиторий

```bash
git clone <ссылка на репозиторий>
cd team-finder-ad
```

### 2. Создать виртуальное окружение и установить зависимости

```bash
python -m venv venv
# source venv/bin/activate       # Linux/Mac
venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

### 3. Создать файл `.env`

```bash
cp .env_example .env
```

Минимальный рабочий `.env` для локальной разработки:

```env
DJANGO_SECRET_KEY=любая-случайная-строка
DJANGO_DEBUG=True

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TASK_VERSION=1
```

Сгенерировать секретный ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Запустить базу данных через Docker

```bash
docker compose up -d
```

Остановить: `docker compose down`

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер разработки

```bash
python manage.py runserver
```

Приложение: http://localhost:8000  
Административная панель: http://localhost:8000/admin/

## Тестовые пользователи

В проекте уже созданы тестовые пользователи. Если база данных пустая — создать их можно командой:

```bash
python manage.py shell -c "
from users.models import User
from projects.models import Project

u1 = User.objects.create_user(email='ivanova@example.com', name='Анна', surname='Иванова', password='password123')
u1.about = 'Бэкенд-разработчик с 3-летним опытом на Python и Django'
u1.save()

u2 = User.objects.create_user(email='petrov@example.com', name='Михаил', surname='Петров', password='password123')
u2.about = 'Фронтенд-разработчик, люблю создавать красивые интерфейсы'
u2.save()

u3 = User.objects.create_user(email='sidorova@example.com', name='Елена', surname='Сидорова', password='password123')
u3.about = 'DevOps-инженер, занимаюсь контейнеризацией и автоматизацией'
u3.save()

p1 = Project.objects.create(name='Трекер задач для команды', description='Веб-приложение для управления задачами', owner=u1, status='open', github_url='https://github.com/example/tracker')
p1.participants.add(u1, u2)

p2 = Project.objects.create(name='Платформа онлайн-курсов', description='Образовательная платформа с видеоуроками и сертификатами', owner=u2, status='open')
p2.participants.add(u2, u3)

p3 = Project.objects.create(name='Аналитический дашборд', description='Интерактивный дашборд для визуализации бизнес-метрик', owner=u3, status='closed')
p3.participants.add(u3, u1)

u1.favorites.add(p2)
u2.favorites.add(p1, p3)
print('Готово!')
"
```

| Роль | Пользователь | Email | Пароль |
|------|-------------|-------|--------|
| Администратор | Системный Администратор | admin@teamfinder.ru | admin123 |
| Обычный пользователь | Анна Иванова | ivanova@example.com | password123 |
| Обычный пользователь | Михаил Петров | petrov@example.com | password123 |
| Обычный пользователь | Елена Сидорова | sidorova@example.com | password123 |
