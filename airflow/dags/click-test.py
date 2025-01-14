from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from clickhouse_driver import Client

def test_clickhouse_connection(**kwargs):
    """
    Function to test the connection to ClickHouse.
    """
    host = kwargs.get('host', 'clickhouse')
    port = kwargs.get('port', 9000)
    user = kwargs.get('user', 'default')
    password = kwargs.get('password', '')
    database = kwargs.get('database', 'default')

    try:
        # Create ClickHouse client
        client = Client(host=host, port=port, user=user, password=password, database=database)

        # Test query
        query = "SELECT version()"
        result = client.execute(query)

        print(f"Successfully connected to ClickHouse. Version: {result[0][0]}")

    except Exception as e:
        print(f"Failed to connect to ClickHouse: {e}")
        raise

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'test_clickhouse_connection',
    default_args=default_args,
    description='A simple DAG to test ClickHouse connection',
    schedule_interval=None,  # Run manually
    start_date=datetime(2024, 12, 30),
    catchup=False,
)

# Define the PythonOperator
clickhouse_test_task = PythonOperator(
    task_id='test_clickhouse_connection_task',
    python_callable=test_clickhouse_connection,
    op_kwargs={
        'host': 'clickhouse',
        'port': 9000,
        'user': 'default',
        'password': '',
        'database': 'default',
    },
    dag=dag,
)

clickhouse_test_task
