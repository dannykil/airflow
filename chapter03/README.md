cp /Users/danniel.kil/Documents/workspace/airflow/chapter03/dags/01_unscheduled.py /opt/anaconda3/lib/python3.12/site-packages/airflow/example_dags/01_unscheduled.py

cat /opt/anaconda3/lib/python3.12/site-packages/airflow/config_templates/default_airflow.cfg
airflow config list
airflow config list --defaults

docker run -it -p 8080:8080 \
-v /Users/danniel.kil/Documents/workspace/airflow/chapter03/dags:/opt/airflow/dags \
--entrypoint=/bin/bash \
--name chapter03 \
apache/airflow:2.10.5-python3.9 \
-c '( \
airflow db init && \
airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email danniel.kil@gmail.com \
); \
airflow webserver & \
airflow scheduler \
'

docker exec -it airflow /bin/bash
