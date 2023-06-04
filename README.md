
1. Скопируйте проект по ссылке:
   - git@github.com:Pixel2022UA/Homework_10.git

2. Откройте проект в PyCharm и установите необходимые зависимости из файла requirements.txt, используя команду 
   - pip install -r requirements.txt

3. __База данных залита на гит__, но так же можно создать новую:
   - python manage.py makemigrations
   - python manage.py migrate

4. __Скопируйте прикрепленный в LMS Hillel файл .env в корневую директорию проекта (в директорию с фалом manage.py).

5. :exclamation: __В PyCharm убедитесь, что вы находитесь в директории, где расположены файлы проекта и файл manage.py__

6. Запустите RabbitMQ в контейнере Docker используя команду: 
   - docker run -d -p 5672:5672 rabbitmq

7. Запустите Celery worker, используя команду:
    - celery -A exchange_rates worker -l INFO

8. Запустите планировщик задач в Celery(если в этом есть необходимость, т.к. файл базы данных залит на гит,
в случае если какие либо api ключи не сработают по причине их лимита на использование у некотрых провайдеров):
   - celery -A exchange_rates beat

9. Запустите проект, используя команду:
   - python manage.py runserver

10. Теперь вы можете открыть веб-браузер и перейти на страницу http://127.0.0.1:8000/exchange/
