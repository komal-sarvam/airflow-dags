from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

from datetime import timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="gujarati_ocr_pipeline",
    default_args=default_args,
    description="Pipeline for Gujarati OCR using YOLOv10, OCR, LLM post-processing and email",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["ocr", "gujarati", "nlp"],
) as dag:

    # Variables (set from Airflow UI or CLI)
    mongo_uri = Variable.get("MONGO_URI")
    bucket_name = Variable.get("BUCKET_NAME")
    gcs_credentials_path = Variable.get("GOOGLE_APPLICATION_CREDENTIALS")

    upload_input = KubernetesPodOperator(
        task_id="upload_input",
        name="upload-input",
        image="gcr.io/YOUR_PROJECT_ID/upload-handler:latest",
        cmds=["python", "upload_and_store.py"],
        env_vars={
            "MONGO_URI": mongo_uri,
            "BUCKET_NAME": bucket_name,
        },
        namespace="airflow",
        get_logs=True,
        is_delete_operator_pod=True,
    )

    yolo_inference = KubernetesPodOperator(
        task_id="yolo_inference",
        name="yolo-infer",
        image="gcr.io/YOUR_PROJECT_ID/yolo-infer:latest",
        cmds=["python", "yolo_inference.py"],
        env_vars={
            "MONGO_URI": mongo_uri,
        },
        namespace="airflow",
        get_logs=True,
        is_delete_operator_pod=True,
    )

    ocr_processing = KubernetesPodOperator(
        task_id="ocr_processing",
        name="ocr-processor",
        image="gcr.io/YOUR_PROJECT_ID/ocr-processor:latest",
        cmds=["python", "run_ocr.py"],
        env_vars={
            "MONGO_URI": mongo_uri,
            "GOOGLE_APPLICATION_CREDENTIALS": gcs_credentials_path,
        },
        namespace="airflow",
        get_logs=True,
        is_delete_operator_pod=True,
    )

    llm_postprocess = KubernetesPodOperator(
        task_id="llm_postprocess",
        name="llm-postprocessor",
        image="gcr.io/YOUR_PROJECT_ID/llm-corrector:latest",
        cmds=["python", "llm_correct.py"],
        env_vars={
            "MONGO_URI": mongo_uri,
        },
        namespace="airflow",
        get_logs=True,
        is_delete_operator_pod=True,
    )

    email_user = KubernetesPodOperator(
        task_id="email_user",
        name="email-user",
        image="gcr.io/YOUR_PROJECT_ID/email-sender:latest",
        cmds=["python", "email_results.py"],
        env_vars={
            "MONGO_URI": mongo_uri,
            "EMAIL_API_KEY": Variable.get("EMAIL_API_KEY"),  # e.g., SendGrid or SMTP
        },
        namespace="airflow",
        get_logs=True,
        is_delete_operator_pod=True,
    )

    upload_input >> yolo_inference >> ocr_processing >> llm_postprocess >> email_user
