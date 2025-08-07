# tests/test_dag.py

from airflow.models import DagBag

def test_churn_pipeline_dag_loads():
    dag_bag = DagBag(dag_folder="airflow/dags", include_examples=False)
    dag = dag_bag.get_dag("churn_sagemaker_pipeline")

    assert dag is not None, "DAG 'churn_sagemaker_pipeline' is not defined"
    assert len(dag.tasks) > 0, "DAG has no tasks"
    assert "train_model" in dag.task_ids, "Missing task: train_model"
