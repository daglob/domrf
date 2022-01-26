import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from psycopg2 import connect, extras
from requests import get

# load environment variables
load_dotenv(dotenv_path=Path('.env'))

# make result paths
Path(os.getenv("PATH_RESULT")).mkdir(parents=True, exist_ok=True)
path_json = f'{os.getenv("PATH_RESULT")}/{os.getenv("PATH_JSON")}'
path_csv = f'{os.getenv("PATH_RESULT")}/{os.getenv("PATH_CSV")}'

# load remote data
data = get('https://randomuser.me/api/?results=500').json()

# write json for check
with open(path_json, 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, indent=4)

conn = connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

clean_data = [x for x in [(item["gender"],
                           item["name"]["title"],
                           item["name"]["first"],
                           item["name"]["last"],
                           item["location"]["city"],
                           item["email"],
                           item["login"]["md5"],
                           item["phone"]) for
                          item in
                          data['results']]]

headers = ["Gender", "Name", "First name", "Last name", "City", "Email", "Md5 login", "Phone number"]

with open(path_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(clean_data)

insert_query = 'INSERT INTO people ("Gender","Name","First name","Last name","City","Email","Md5 login","Phone number") values %s'
cur.execute('TRUNCATE TABLE people;')
extras.execute_values(cur, sql=insert_query, argslist=clean_data)
conn.commit()
conn.close()
