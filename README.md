# jqmw565

## Описание проекта
1. **Стек** - Python 3.12.6, Flask, Jquery, HTML, CSS, PostgreSQL, Selenium, Gunicorn + Nginx 
2. **Функционал** - проект предусматривает динамическое добавление полей ввода (ajax) и отправку данных формы через кнопку. После нажатия на кнопку _OK_ уведомления об успешной отправке данных _**автоматически**_ происходит перенаправление на страницу с выводом всех данных из БД PostgreSQL.

    > [!TIP]
    > превью проекта размещено после инструкции по развертыванию проекта 

## Инструкция по развертыванию flask-проекта 

### Шаг 1. Предварительные требования

1. Ubuntu 20.04+
2. Установленный git
3. Доступ к терминалу с правами суперпользователя (`sudo`)

### Шаг 2. Клонирование репозитория
1. Запустить терминал
2. Перейти в директорию, где будет храниться проект:
   
   `cd /home/.../`

3. Далее для развертывания проекта необходимо клонировать репозиторий с исходным кодом, используя комманду:

    `git clone https://github.com/anastasiaserguta/jqmw565.git`

### Шаг 3. Установка и запуск PostgreSQL

1. Используя команды обновления (при необходимости) доступных официальных репозиториев и установленных пакетов (`sudo apt update` + `sudo apt upgrade`) установить PostgreSQL:
    
    `sudo apt install postgresql postgresql-contrib`

2. Запустить PostgreSQL и добавить службу в автозапуск вместе с системой:
   
    `sudo systemctl start postgresql`

    `sudo systemctl enable postgresql`

### Шаг 4. Настройка PostgreSQL

1. Для хранения данных данного проекта предполагается использование базы данных PostgreSQL, доступной на локальном сервере. В этой связи необходимо ее создать и подключить к проекту, используя приведенные ниже команды.
   
2. Зайти в интерактивную сессию PostgreSQL под стандартными пользователем `postgres` при помощи команды:
   
    `sudo -iu postgres psql`

3. Создать базу данных с именем `flaskdb`:

    `CREATE DATABASE flaskdb;`

4. Создать пользователя базы данных для проекта, где `ast` - имя пользователя, `'1234'` - пароль для доступа:

    `CREATE USER ast PASSWORD '1234';`

5. Предоставляем созданному пользователю все права для работы с базой и указываем его в качестве владельца базы:

    `GRANT ALL PRIVILEGES ON DATABASE flaskdb TO ast;`

    `ALTER DATABASE flaskdb OWNER TO ast;`

6. Проверяем наличие созданной базы и ее владельца в списке доступных баз командой `\l`. Выходим из интерактивного режима командой `\q`.

### Шаг 5 (опциальный). Установка python 3.12, pip и venv (при их отсутствии)

1. Для работы проекта необходимо установить `python 3.12+`, пакетный менеджер `pip`, а также пакет для создания виртуального окружения.

    > [!TIP]
    > В Ubuntu `python 3` поставляется вместе с системой. Проверить версию `python` можно при помощи команды `python3 --version`. 

    > [!TIP] 
    > К примеру, c Ubuntu 20.04.6 поставляется `python 3.8.10`. Вместе с тем, проект написан на `python 3.12.6`, в связи с чем рекомендуется установить его.

2. В стандартных репозиториях нет `python 3.12`, для этого необходимо использовать другой источник. Добавить репозиторий с различными версиями `python` можно командами:

    `sudo add-apt-repository ppa:deadsnakes/ppa`

    `sudo apt update`
    
    `sudo apt upgrade`

    установка `python 3.12.6`:

    `sudo apt install -y python3.12.6`

    > [!IMPORTANT]
    > В зависимости от настроек системы может потребоваться выполнение и других команд исходя из сообщений терминала.
    
    > [!NOTE]
    > флаг `-y` предполагает автоматическое подтверждение всех запросов, которые могут возникнуть в процессе установки. 

3. Для установки `pip` и `venv` (если они не установлены) необходимо выполнить команды:

    `sudo apt install -y python3.12-distutils` - установка необходимых компонентов

    `wget https://bootstrap.pypa.io/get-pip.py` - загрузка скрипта для установки `pip`

    `sudo python3.12 get-pip.py` - установка `pip`

    `sudo apt install -y python3.12-venv` - установка пакета для работы с виртуальным окружением

### Шаг 6. Активация виртуального окружения и установка зависимостей

1. В терминале перейти в директорию с кодом проекта и создать виртуальное окружение:

    `python3.12 -m venv .env`

2. Активировать виртуальное окружение и установить все используемые для проекта зависимости из файла `requirements.txt`:

    `source .env/bin/activate`

    `pip install -r requirements.txt`

### Шаг 7. Инициализация базы данных и подключение к ней через переменные окружения

1. Для создания таблицы базы данных, необходимой для хранения данных проекта необходимо запустить скрипт `init_db.py` командой:

    `python3 init_db.py`

2. Далее важно экспортировать необходимые для подключения к базе данные в переменные виртуального окружения:

    `EXPORT POSTGRES_DB='flaskdb'`
    `EXPORT USERNAME_DB='ast'`
    `EXPORT PASSWORD_DB='1234'`

    > [!NOTE]
    > Это первоначальная настройка подключения базы к приложению, поскольку переменные окружения в `.env` экспортируются на текущий сеанс и после перезагрузки/прекращения сеанса будут недоступны.

### Шаг 8. Тестовый запуск

1. Для проверки, что все установлено правильно, можно локально запустить приложение используя сервер `gunicorn` командой:
   
    `gunicorn --bind 0.0.0.0:5000 wsgi:app`

2. Так как приложение запускается на локальном сервере, оно должно быть доступно по адресу: `http://127.0.0.1:5000/`

    > [!TIP]
    > Для автоматизации тестирования веб-приложение поставляется с тестами (модуль `unittest` + `selenium`) для предустановленного на Ubuntu браузера Firefox. Их можно запустить из файла `for_test.py`.

3. Если все настроено верно и работает останавливаем сервер `^C` и деактивируем `.env` командой `deactivate`.

### Шаг 9. Разворачиваем flask-проект на сервере gunicorn

1. Настраиваем конфиг-файл для автоматического запуска `.env.` для gunicorn, используя встроенные редактор `nano`:

    `sudo nano /etc/systemd/system/flask_proj.service`

    в открывшемся окне прописываем следующие данные (с учетом директорий Вашего сервера):

    ```
    [Unit]
    Description=Gunicorn instance to serve flask_proj
    After=network.target

    [Service]
    User=your_user
    Group=www-data
    WorkingDirectory=/home/your_path/flask_proj
    Environment="PATH=/home/your_path/flask_proj/.env/bin"
    Environment="POSTGRES_DB=flaskdb"
    Environment="USERNAME_DB=ast"
    Environment="PASSWORD_DB=1234"
    ExecStart=/home/your_path/flask_proj/.env/bin/gunicorn --workers 3 --bind unix:/home/your_path/flask_proj.sock -m 007 app:app

    [Install]
    WantedBy=multi-user.target
    ```

    > [!NOTE]
    > где `your_path` путь на Вашем сервере.

    > [!IMPORTANT]
    > здесь мы также прописываем наши переменные окружения во избежание ошибок с подключением к базе данных по причине отсутствия доступа к переменным.

    > [!NOTE]
    > закрываем и сохраняем файл `^X`, `Y`, `enter`.

2. Запускаем сервер и проверяем его состояние:

    `sudo systemctl start flask_proj`
    `sudo systemctl status flask_proj`

    > [!TIP]
    > при необходимости можно настроить автозапуск сервера вместе с ОС командой `sudo systemctl enable flask_proj`

### Шаг 10. Установка и подключение nginx

1. Для начала необходимо установить `nginx`:

    `sudo apt -y install nginx`
    
2. Далее необходимо создать конфиг-файл для `nginx`. Используя команду:

    `sudo nano /etc/nginx/sites-available/flask_proj`

    откроем редактор `nano` и пропишем следующие данные:

    ```
    server {
    listen 80;
    server_name 127.0.0.1;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/your_path/flask_proj.sock;
        }
    }

    ```

    > [!NOTE]
    > указываем адреc, на который будет реагировать nginx `127.0.0.1`, а также инструкцию для обработки запросов, то есть `nginx` будет перенаправлять поступающие запросы к запущенному на `gunicorn` flask-приложению.

3. Закроем указанный выше файл с сохранением данных и добавим ссылку на файл конфигурации, чтобы `nginx` мог использовать созданную конфигурацию для обслуживания приложения:

    `sudo ln -s /etc/nginx/sites-available/flask_proj /etc/nginx/sites-enabled`

    добавим пользователя `www-data` в группу текущего пользователя для доступа к `gunicorn`:

    `sudo usermod -a -G ${USER} www-data` 

    проверим корректность написанных в файле данных:

    `nginx -t`

    и перезагрузим `nginx`, если все в порядке:

    `nginx -s reload`

5. Выполним еще некоторые настройки и перейдем по адресу доступа веб-приложения:

    `sudo ufw delete allow 5000` - удаляем доступ по порту 5000

    `sudo ufw allow 'Nginx Full'` - открываем подключение через `nginx` 

6. При переходе на наш локальный адрес `http://127.0.0.1/` будет доступно веб-приложение flask:

![preview gif](/preview/preview.gif)

***
#### Cтатус сервера, а также журналы логирования `nginx` и `gunicorn`:

![status png](/preview/status_gunicorn.png)

![log gunicorn png](/preview/log_gunicorn.png)

![log nginx png](/preview/log_nginx.png)

> [!NOTE]
> журнал ошибок `nginx` пуст
***




    




    