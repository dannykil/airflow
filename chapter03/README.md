# Chapter 3

Code accompanying Chapter 3 of the book 'Data pipelines with Apache Airflow'.

## Contents

This code example contains the following DAGs:

- 01_unscheduled.py - Initial DAG without schedule.
- 02_daily_schedule.py - Same DAG following a daily schedule.
- 03_different_start_date.py - DAG with adjusted start date.
- 04_with_end_date.py - Modified DAG with an end date.
- 05_time_delta_schedule.py - DAG that uses a timedelta for the schedule interval.
- 06_query_with_dates.py - DAG including hard-coded dates in the query.
- 07_templated_query.py - Replaces hard-coded dates with templated execution dates.
- 08_templated_query_ds.py - Uses shorthands for the templated execution dates.
- 09_templated_path.py - Uses templating for the file paths as well.
- 10_full_example.py - Filly completed example, including 'sending' of statistics.

## Usage

To get started with the code examples, start Airflow in docker using the following command:

    docker-compose up --build
    docker compose up --build

Wait for a few seconds and you should be able to access the examples at http://localhost:8080/.

To stop running the examples, run the following command:

    docker-compose down -v
    docker compose down -v

## Usage2 - danny

# 1) Stopping all of the containers

docker stop $(docker ps -qa)

# 2) Deleting all of the containers

docker rm $(docker ps -qa)

# 3) Deleteing all of the images

docker rmi $(docker images -qa)

# 4) Deleteing all of the volumes

docker volume rm $(docker volume ls -qf dangling=true)

# 5) Deleteing all of configurations like network

docker system prune -f

# 6) Check results

docker ps -a
docker images
docker volume ls
docker network ls

# 제미나이 질문1

제공된 Airflow DAG 코드에서 {{ds}} 및 {{next_ds}}는 Airflow의 Jinja 템플릿 매크로입니다. 이 매크로들은 Airflow 스케줄러에 의해 실제 날짜 데이터로 변환됩니다. 변환 과정은 다음과 같습니다.

1. DAG 파싱 및 스케줄링:
   Airflow 스케줄러는 DAG 파일을 주기적으로 파싱하여 DAG 정의를 읽어옵니다.
   DAG의 schedule_interval에 따라 DAG 실행 스케줄을 생성합니다.
   각 DAG 실행은 특정 execution_date를 가지며, 이는 해당 DAG 실행이 처리해야 하는 데이터의 시간 범위를 나타냅니다. 2. Jinja 템플릿 렌더링:

2) Jinja 템플릿 렌더링:
   DAG 실행 시, Airflow는 BashOperator의 bash_command와 같은 템플릿 필드를 Jinja 템플릿 엔진을 사용하여 렌더링합니다.
   {{ds}} 매크로는 execution_date를 'YYYY-MM-DD' 형식의 문자열로 변환합니다.
   {{next_ds}} 매크로는 execution_date의 다음 날짜를 'YYYY-MM-DD' 형식의 문자열로 변환합니다.

# 제미나이 질문2

Jinja2는 파이썬 기본 패키지가 아니며, 별도로 설치해야 하는 패키지입니다. Airflow 프로젝트에서 Jinja2를 명시적으로 설치하거나 import하지 않았음에도 불구하고 Jinja 템플릿을 사용할 수 있는 이유는 Airflow가 Jinja2를 의존성 패키지로 포함하고 있기 때문입니다.

1. Airflow의 Jinja2 의존성:
   Airflow는 DAG 정의, 템플릿 변수, 매크로 등을 처리하기 위해 Jinja2를 사용합니다.
   Airflow를 설치할 때, Airflow의 의존성 패키지 목록에 Jinja2가 포함되어 자동으로 설치됩니다.
   따라서 Airflow 프로젝트에서 Jinja2를 직접 설치하거나 import하지 않아도 Jinja 템플릿을 사용할 수 있습니다.
   Jinja2의 역할:

2. Jinja2의 역할:
   Jinja2는 파이썬 템플릿 엔진으로, 문자열 템플릿에 변수와 표현식을 삽입하여 동적으로 문자열을 생성하는 데 사용됩니다.
   Airflow에서는 Jinja2를 사용하여 DAG 정의, Task 설정, 변수 등을 동적으로 생성하고 관리합니다.
   {{ ... }}와 같은 Jinja 템플릿 문법을 사용하여 Airflow 매크로, 변수, 컨텍스트 변수 등을 사용할 수 있습니다.

# docker가 설치된 경우에도 command not found: docker가 발생하는 경우

export PATH=/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin
export PATH="$PATH:/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin"
