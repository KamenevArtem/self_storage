# self_storage
 MVP под проект сервиса хранения вещей на складе.  
 Версия Python 3.9 и выше.

## Как установить
- Установка зависимостей  
```
pip3 install -r requirements.txt
```
- Заполнение переменных окружения `TG_CUSTOMER_BOT_TOKEN` и `TG_OWNER_BOT_TOKEN`:
```
TG_CUSTOMER_BOT_TOKEN="токен бота для заказчиков"
TG_OWNER_BOT_TOKEN="токен бота для владельца"
```
- Применение миграций для создания базы:
```
python3 manage.py migrate
```
- Тестовый запуск админки
```
python3 manage.py manage.py runserver
```
- Запуск ботов:
```
python3 manage.py bot
```
## Цель проекта
Запуск тестовой среды для выявления потребности в сервисе.  
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/)

