Python 3+

---
Есть 2 способа получить данные:
1. Используя преднастроенные контейнеры и Spark
2. Используя python окружения (на локальной машине, например)

> Для корректной работы обоих способов, требуется заполнить значение переменных в файле .env

---

# Environment

Создаем/изменяем файл .env в корне проекта _(см. .env.example для примера)_

```dotenv
# for postgresql database
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=

# for containers only
DB_HOST=

# results
PATH_RESULT=./result        # директория, где будут лежать файлы с результатами
PATH_CSV=result.csv         # имя файла и разрешения для сохранения данных в формате CSV
PATH_JSON=json_data.json    # результат запроса к сервису https://randomuser.me/api/?results=500
```

---

# With Spark

## Install

> docker-compose up -d --build

## Calculate data | Run

> docker-compose exec spark bash -c "spark-submit main.py"

---

# "Vanilla" python

## Install

Устанавливаем библиотеки в окружение:

```
pip install requests
pip install python-dotenv
pip install psycopg2-binary
```

## Calculate data | Run

```
python vanilla.py
```