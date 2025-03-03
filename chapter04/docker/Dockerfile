ARG AIRFLOW_BASE_IMAGE="apache/airflow:2.10.5-python3.11"
FROM ${AIRFLOW_BASE_IMAGE}

# RUN pip install --user --no-cache-dir \
#     apache-airflow-providers-postgres==1.0.0

RUN pip install --upgrade pip

# RUN pip install --user --no-cache-dir 
# RUN pip install --user --no-cache-dir base
# RUN pip install --no-cache-dir
# Docker 이미지 내에서 가상 환경을 사용하는 경우, --user 옵션을 제거하고 패키지를 가상 환경에 직접 설치합니다.
RUN pip install --no-cache-dir base

# RUN apache-airflow-providers-postgres==1.0.0
# RUN pip install apache-airflow-providers-postgres==1.0.0
RUN pip install apache-airflow-providers-postgres
