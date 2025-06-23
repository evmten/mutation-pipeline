from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime

# Arguments
default_args = {
    'start_date': datetime(2025, 5, 1),
}

# Define the DAG
with DAG(
    dag_id='ingest_dag',
    default_args=default_args,
    schedule_interval=None, # Manual trigger
    catchup=False,
    tags=['mutation'],
) as dag:
    
    # Ingestion task
    ingest_task = BashOperator(
        task_id='run_streaming_ingestion',
        bash_command='python /opt/airflow/scripts/ingest_data.py'
    )

