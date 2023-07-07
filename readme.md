```bash
python3 -m venv venv
```
1. Активировать виртуальное окружение
```bash
source venv/bin/activate
```
2. Установить зависимости проекта, указанные в файле `requirements.txt`
```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate
```
```bash
python manage.py loaddata data.json
```
14. Запустить сервер
```bash
python manage.py runserver
```
Для профиля пользователя сделайте вывод истории платежей, расширив сериализатор для вывода списка платежей.