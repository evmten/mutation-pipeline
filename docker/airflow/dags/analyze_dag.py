from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 5, 1),
}

with DAG(
    dag_id='analyze_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['mutation'],
) as dag:

    analyze_task = BashOperator(
        task_id='run_mutation_analysis',
        bash_command='python /opt/airflow/scripts/analyze_mutations.py'
    )