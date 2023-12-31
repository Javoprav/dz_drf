```bash
python3 -m venv venv
```
Активировать виртуальное окружение
```bash
source venv/bin/activate
```
Установить зависимости проекта, указанные в файле `requirements.txt`
```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate
```
```bash
python manage.py loaddata data1.json
```
```bash
python3 manage.py create_user
```
Запустить сервер
```bash
python manage.py runserver
```
Собрать и запустить образ docker-compose
```bash
 docker-compose up -d --build
```
__________________________________________

Задание
Контекст
Для быстрого масштабирования проекта применяется контейнеризация. Для этого вам предстоит «завернуть» ваш проект в Docker и настроить на самостоятельный запуск.

Критерии приемки курсовой работы
Для разных сервисов создали отдельные контейнеры (django, postgresql, redis, celery, при необходимости список можно самостоятельно расширять).
Всё оформили в файле docker-compose, при необходимости создали вспомогательные Dockerfiles.
Проект готов быть размещенным на удаленном сервере:
его можно запустить по инструкции, приложенной в Readme-файл;
для запуска не требуется дополнительных настроек.
Решение выложили на GitHub.
Для выполнения задания используйте курсовой проект, над которым вы работали в курсе DRF.

Задание
Cоздайте отдельные контейнеры для сервисов в проекте.

Как минимум для следующих сервисов:

Django,
PostrgeSQL,
Redis,
Celery.
Как максимум — для всех сервисов проекта.

Весь проект должен запускаться одной командой и при этом иметь возможность быть перенесенным на отдельный удаленный сервер для запуска на нём.
__________________________________________


_________________________________

Домашнее задание 24.1 Вьюсеты и дженерики
Задание 1
Создайте новый Django-проект, подключите DRF и внесите все необходимые настройки.

Задание 2
Создайте следующие модели:

Пользователь:
все поля от обычного пользователя, но авторизацию заменить на email;
телефон;
город;
аватарка.
Курс:
название,
превью (картинка),
описание.
Урок:
название,
описание,
превью (картинка),
ссылка на видео.
Задание 3
Опишите CRUD для моделей курса и урока, но при этом для курса сделайте через ViewSets, а для урока — через Generic-классы.

Для работы контроллеров опишите простейшие сериализаторы.

Работу каждого эндпоинта необходимо проверять с помощью Postman.

Также на данном этапе работы мы не заботимся о безопасности и не закрываем от редактирования объекты и модели даже самой простой авторизацией.

* Дополнительное задание
Реализуйте эндпоинт для редактирования профиля любого пользователя на основе более привлекательного подхода для личного использования: Viewset или Generic.

_______________________________

Домашнее задание 24.2 Сериализаторы

Задание 1
Для модели курса добавьте в сериализатор поле вывода количества уроков.

Задание 2
Добавьте новую модель.

Платежи:

пользователь,
дата оплаты,
оплаченный курс или урок,
сумма оплаты,
способ оплаты — наличные или перевод на счет.
Запишите в эту модель данные через инструмент фикстур или кастомную команду.

Задание 3
Для сериализатора для модели курса реализуйте поле вывода уроков.

Задание 4
Настройте фильтрацию для эндпоинтов вывода списка платежей с возможностями:

менять порядок сортировки по дате оплаты,
фильтровать по курсу или уроку,
фильтровать по способу оплаты.
* Дополнительное задание
Для профиля пользователя сделайте вывод истории платежей, расширив сериализатор для вывода списка платежей.
_______________________________

Домашнее задание 25.1 Права доступа в DRF
Задание 1
Настройте в проекте использование JWT авторизации и закройте каждый эндпоинт авторизацией.

Задание 2
Заведите группу модераторов и опишите для нее права работы с любыми уроками или курсами, но без возможности их удалять и создавать новые. Заложите функционал такой проверки в контроллеры.

Задание 3
Опишите права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть и редактировать только свои курсы и уроки.

Заводить группы лучше через админку и не реализовывать для этого дополнительных эндпоинтов.