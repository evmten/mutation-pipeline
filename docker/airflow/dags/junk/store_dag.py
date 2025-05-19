# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from datetime import datetime

# default_args = {
#     'start_date': datetime(2025, 5, 1),
# }

# with DAG(
#     dag_id='store_flags_dag',
#     default_args=default_args,
#     schedule_interval=None,
#     catchup=False,
#     tags=['mutation'],
# ) as dag:

#     store_task = BashOperator(
#         task_id='store_mutation_flags_to_postgres',
#         bash_command='python /opt/airflow/scripts/store_mutation_flags.py'
#     )
