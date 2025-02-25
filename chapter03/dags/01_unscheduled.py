from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="01_unscheduled", start_date=datetime(2019, 1, 1), schedule_interval=None
)

# curl -o [저장할_파일명] [다운로드할_URL]
fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        # "mkdir -p /data/events && "
        # "curl -o /data/events.json http://events_api:5000/events"
        "mkdir -p /opt/airflow/data && "
        "curl -o /opt/airflow/data/events.json https://dev-web-213242029674.us-central1.run.app/api/getIP"
        # "mkdir /Users/danniel.kil/Documents/workspace/airflow/chapter03/data/events && "
        # "curl -o /Users/danniel.kil/Documents/workspace/airflow/chapter03/data/events.json http://events_api:5000/events"
    ),
    dag=dag,
)


def _calculate_stats(input_path, output_path):
    """Calculates event statistics."""

    print("1")
    Path(output_path).parent.mkdir(exist_ok=True)
    print("2")
    events = pd.read_json(input_path)
    print("3")
    stats = events.groupby(["date", "user"]).size().reset_index()
    print("4")
    stats.to_csv(output_path, index=False)
    print("5")


calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={"input_path": "/opt/airflow/data/events.json", "output_path": "/opt/airflow/data/stats.csv"},
    dag=dag,
)

fetch_events >> calculate_stats