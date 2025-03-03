# """
# Documentation of pageview format: https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageviews
# """

from urllib import request

import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator 
# from airflow.providers.postgres.hooks.postgres import PostgresHook

dag = DAG(
    dag_id="listing_4_20",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
    template_searchpath="/tmp",
    max_active_runs=1,
)


def _get_data(year, month, day, hour, output_path):
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    request.urlretrieve(url, output_path)


get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        "year": "{{ execution_date.year }}",
        "month": "{{ execution_date.month }}",
        "day": "{{ execution_date.day }}",
        "hour": "{{ execution_date.hour }}",
        "output_path": "/tmp/wikipageviews.gz",
        # "output_path": "/tmp/wikipageviews.tgz",
        # "output_path": "/tmp/wikipageviews.tar",
    },
    dag=dag,
)


extract_gz = BashOperator(
    task_id="extract_gz", bash_command="gunzip --force /tmp/wikipageviews.gz", dag=dag
    # task_id="extract_gz", bash_command="gunzip --force /tmp/wikipageviews.tgz", dag=dag
    # task_id="extract_gz", bash_command="gunzip --force /tmp/wikipageviews.tar", dag=dag
)


def _fetch_pageviews(pagenames, execution_date):
    result = dict.fromkeys(pagenames, 0)
    # print("result before for : ", result)
    with open("/tmp/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en" and page_title in pagenames:
                result[page_title] = view_counts
                # print("result : ", result)

    with open("/tmp/postgres_query.sql", "w") as f:
        for pagename, pageviewcount in result.items():
            # print("pagename : {}, pageviewcount : {}".format(pagename, pageviewcount))

            f.write(
                "INSERT INTO pageview_counts VALUES ("
                f"'{pagename}', {pageviewcount}, '{execution_date}'"
                ");\n"
                # "INSERT INTO pageview_counts (pagename, pageviewcount, datetime) VALUES ("
                # f"'{pagename}', {pageviewcount}, '{execution_date}'"
                # ");\n"
            )


fetch_pageviews = PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={"pagenames": {"Google", "Amazon", "Apple", "Microsoft", "Facebook"}},
    dag=dag,
)

write_to_postgres = SQLExecuteQueryOperator(
    task_id="write_to_postgres",
    # postgres_conn_id="my_postgres",
    conn_id="my_postgres",
    sql="postgres_query.sql",
    dag=dag,
)

# def insert_dag_status(dag_name, flag, execution_date_value):
#     hook = PostgresHook(postgres_conn_id='my_postgres') #DB 연결, 설정해준 connection id 입력
#     conn=hook.get_conn()
#     cursor=conn.cursor()
#     cursor.execute(
#         # "INSERT INTO test.airflow_test (dag_name, flag, execution_time) VALUES (%s, %s, %s)", (dag_name, flag, execution_date_value)
#         # "INSERT INTO pageview_counts (pagename, pageviewcount, execution_date) VALUES (%s, %s, %s)", (pagename, pageviewcount, execution_date)
#         # "INSERT INTO pageview_counts (pagename, pageviewcount, datetime) VALUES (%s, %s, %s)", (dag_name, flag, execution_date_value)
#         "INSERT INTO pageview_counts (pagename, pageviewcount, datetime) VALUES (%s, %s, %s)", (dag_name, 1, execution_date_value)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

# insert_dag1_status=PythonOperator(
#         task_id='insert_dag1_status',
#         python_callable=insert_dag_status,
#         op_args=['listing_4_20', 'S', '{{ts}}'], # ts : DAG 실행 시각, YYYY-MM-DDTHH:MM:SS
#     )

get_data >> extract_gz >> fetch_pageviews >> write_to_postgres
# get_data >> extract_gz >> fetch_pageviews
# get_data >> extract_gz >> fetch_pageviews >> insert_dag1_status


# get_data

# 1)
# CREATE TABLE pageview_counts (
#     pagename VARCHAR(255),
#     pageviewcount INTEGER,
#     datetime TIMESTAMP WITH TIME ZONE
# );

# 2) postgres 패키지 설치
# pip install apache-airflow-providers-postgres
# pip show apache-airflow-providers-postgres

# 3) connection 정보 생성(web-server에서 진행)
# airflow connections add \
#     --conn-type postgres \
#     --conn-host postgres \
#     --conn-port 5432 \
#     --conn-schema airflow \
#     --conn-login airflow \
#     --conn-password airflow \
#     my_postgres

# 4) airflow.cfg 내 test_connection = Enabled 로 변경(web-server에서 진행)
# 4.1) docker exec -u 0 -it <container_id> /bin/bash
# 4.2) apt-get update
# 4.3) apt-get install vim
# 4.4) vim 편집기 내 텍스트 검색 : / 입력 후 엔터
# 4.5) test_connection = Enabled
# 4.6) web-server 재시작




# show databases = \l
# use database = \c airflow
# list tables = \dt
# select * from pageview_counts;
# select count(*) from pageview_counts;
# delete from pageview_counts;