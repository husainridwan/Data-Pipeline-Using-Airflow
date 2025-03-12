from datetime import datetime, timedelta
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from extract import extract_zillow_data

# Get the current date and time
now = datetime.now()
dt_now_str = now.strftime("%Y%m%d%H%M%S")

# Load JSON file
with open('/home/ubuntu/airflow/api.json') as f:
    api_host_key = json.load(f)

s3_bucket = 'zillow-cleaned-data'

# Define default arguments
default_args = {
                'owner': 'airflow',
                'depends_on_past': False,
                'start_date': datetime(2025, 2, 17),
                'email': ['silentbazaar007@gmail.com'],
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 1,
                'retry_delay': timedelta(minutes=5),
                }

# Define the DAG
with DAG(
        'zillowETL',
        default_args=default_args,
        description='An ETL DAG using Zillow API',
        schedule_interval='@daily',
        catchup=False
        ) as dag:

# Define the tasks
        extract_data = PythonOperator(
                            task_id='extractData',
                            python_callable=extract_zillow_data,
                            op_kwargs={'url':"https://zillow56.p.rapidapi.com/search", 
                                        'querystring':{"location":"houston, tx"}, 'headers': api_host_key, 'date_string': dt_now_str})

        load_to_s3 = BashOperator(
                            task_id='loadToS3',
                            bash_command='aws s3 mv {{ ti.xcom_pull("extractData")[0] }} s3://rho-zillow-bucket/')

        is_file_in_s3 = S3KeySensor(
                            task_id='isFileInS3',
                            bucket_name=s3_bucket,
                            bucket_key='{{ ti.xcom_pull("extractData")[1] }}',
                            aws_conn_id='aws_s3_conn',
                            wildcard_match=False,
                            timeout=300,
                            poke_interval=10)

        transfer_to_redshift = S3ToRedshiftOperator(
                            task_id='transferToRedshift',
                            schema='public',
                            table='zillow',
                            s3_bucket=s3_bucket,
                            s3_key='{{ ti.xcom_pull("extractData")[1] }}',
                            copy_options=['csv IGNOREHEADER 1'],
                            aws_conn_id='aws_s3_conn',
                            redshift_conn_id='redshift_conn',)  
        # Set the task dependencies
        extract_data >> load_to_s3 >> is_file_in_s3 >> transfer_to_redshift