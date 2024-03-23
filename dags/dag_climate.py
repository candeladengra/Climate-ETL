from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator

from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from scripts.main import insert_forecast_data, send_email

default_args = {"retries": 3, "retry_delay": timedelta(minutes=1)}

with DAG(
    dag_id="dag_climate",
    start_date=datetime(2024, 3, 1),
    catchup=True,
    schedule_interval="0 0 * * *",
    default_args=default_args,
) as dag:

    create_tables_task = PostgresOperator(
        task_id="create_locations_and_forecast_tables",
        postgres_conn_id="coderhouse_connection",
        sql=["create_locations_table.sql","populate_locations_table.sql", "create_forecast_table.sql"],
        hook_params={"options": "-c search_path=candeladolores_coderhouse"},
    )

    insert_forecast_data_task = PythonOperator(
        task_id="insert_forecast_data",
        python_callable=insert_forecast_data,
        provide_context=True,
        on_success_callback=send_email,
    )

    create_tables_task >> insert_forecast_data_task
