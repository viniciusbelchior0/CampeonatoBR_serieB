from airflow import DAG 
from airflow.operators.python_operator import PythonOperator
import pendulum
import ingestao_dados_serieb
import transformacao_dados_modelagem

with DAG(
    "campeonato-brasileiro_serieb",
    start_date=pendulum.datetime(2024, 5, 1, tz="UTC"),
    schedule_interval='0 12 * * 2,6', # executa ao meio-dia às terças-feiras e aos sábados
) as dag:

    tarefa_2 = PythonOperator(
        task_id = 'extrai_dados',
        python_callable = extrai_dados,
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )

    obter_dfp = BashOperator(
        task_id = 'obter_dfp',
        bash_command = 'Rscript C:/Users/NOTEBOOK CASA/Desktop/cvm_DFPs/obter_dfp.R'
    )

    obter_cias >> obter_dfp