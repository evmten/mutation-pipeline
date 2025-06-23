from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime

# Arguments
default_args = {
    'start_date': datetime(2025, 5, 1),
}

# Define the DAG
with DAG(
    dag_id='transform_dag',
    default_args=default_args,
    schedule_interval=None, # Manual trigger
    catchup=False,
    tags=['mutation'],
) as dag:

    # Transformation task
    transform_task = BashOperator(
        task_id='run_transform_script',
        bash_command='python /opt/airflow/scripts/transform_data.py'
    )
