from airflow.models import DagBag

def test_churn_pipeline_dag_loads():
    dag_bag = DagBag(dag_folder="airflow/dags", include_examples=False)

    # Make sure the DAG loaded without import errors
    assert dag_bag.import_errors == {}, f"DAG import errors: {dag_bag.import_errors}"

    # Validate the expected DAG exists
    assert "churn_sagemaker_pipeline" in dag_bag.dags

    dag = dag_bag.dags["churn_sagemaker_pipeline"]
    assert dag is not None
    assert len(dag.tasks) > 0
