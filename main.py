import json
import os
from pathlib import Path

import pyspark.sql as pySparkSql
from dotenv import load_dotenv
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

# create spark session
spark = pySparkSql. \
    SparkSession.builder.appName('dom.rf-test'). \
    master('local'). \
    getOrCreate()
rdd = spark.sparkContext.parallelize([{"Gender": item["gender"],
                                       "Name": item["name"]["title"],
                                       "First name": item["name"]["first"],
                                       "Last name": item["name"]["last"],
                                       "City": item["location"]["city"],
                                       "Email": item["email"],
                                       "Md5 login": item["login"]["md5"],
                                       "Phone number": item["phone"]} for item in data['results']])

# create dataframe
df = spark.createDataFrame(rdd)

# to csv
df.toPandas().to_csv(path_csv, header=True, index=False)

# to db
df.write.format("jdbc") \
    .option("url", f'jdbc:postgresql://{os.getenv("DB_HOST")}:5432/{os.getenv("POSTGRES_DB")}') \
    .option("driver", "org.postgresql.Driver") \
    .option("dbtable", f'people') \
    .option("user", f'{os.getenv("POSTGRES_USER")}') \
    .option("password", f'{os.getenv("POSTGRES_PASSWORD")}') \
    .mode('overwrite').save()
