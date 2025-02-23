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

docker exec -it chapter03 /bin/bash

cron
0 \* \* \* _ = 매시간(정시)
0 0 _ \* _ = 매일(자정)
0 0 _ _ 0 = 매주(일요일 자정)
0 0 1 _ _ = 매월 1일 자정
45 23 _ _ SAT = 매주 토요일 23시 45분
0 0 _ _ MON, WED, FRI = 매주 월, 수, 금 자정
0 0,12 _ \* \* = 매일 자정, 오후 12시

@once
@hourly
@daily
@weekly
@monthly
@yearly
