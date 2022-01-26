FROM docker.io/bitnami/spark:3
USER root
RUN apt-get update -y && apt-get upgrade -y && apt-get install wget -y
RUN pip install requests
RUN pip install pandas
RUN pip install python-dotenv
RUN cd /opt/bitnami/spark/jars && wget https://jdbc.postgresql.org/download/postgresql-42.2.24.jar
RUN pip install psycopg2-binary
WORKDIR /opt/bitnami/spark
USER 1000