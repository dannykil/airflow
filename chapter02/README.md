1. command line

1) airflow 패키지 설치
   pip install apache-airflow
   /opt/anaconda3/bin/airflow
   /opt/anaconda3/lib/python3.12/site-packages/airflow/example_dags

2) airflow db(airflow 상태를 저장하는 데이터베이스) 초기화
   airflow db init

3) 사용자(admin // admin) 생성
   airflow users create --username admin --firstname Anonymous --lastname Admin --role Admin --email danniel.kil@gmail.com

4) 샘플파일 복사
   cp download_rocket_launches.py ~/airflow/dags

5) airflow 스케줄러/웹서버 시작
   airflow webserver
   airflow scheduler

6) 웹서버 이동
   http://localhost:8080

docker run -it -p 8080:8080 \
-v /Users/danniel.kil/Documents/workspace/airflow/chapter02/dags/download_rocket_launches.py:/opt/airflow/dags/download_rocket_launches.py \
--entrypoint=/bin/bash \
--name airflow \
apache/airflow:2.10.5-python3.9 \
-c '( \
airflow db init && \
airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email danniel.kil@gmail.com \
); \
airflow webserver & \
airflow scheduler \
'

cp /Users/danniel.kil/Documents/workspace/airflow/chapter02/dags/download_rocket_launches.py /opt/anaconda3/lib/python3.12/site-packages/airflow/example_dags/download_rocket_launches.py

mkdir /opt/anaconda3/lib/python3.12/site-packages/airflow/example_dags/education

ls -l | grep ^- | wc -l

docker exec -it chapter03 /bin/bash
