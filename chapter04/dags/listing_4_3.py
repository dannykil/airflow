import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

# 태스크에서 사용할 수 있는 콘텍스트 변수 출력
dag = DAG(
    dag_id="listing_4_03",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
)


def _print_context(**kwargs):
    print(kwargs)


print_context = PythonOperator(
    task_id="print_context", python_callable=_print_context, dag=dag
)
