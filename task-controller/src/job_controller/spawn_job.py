import concurrent.futures

import shortuuid
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from src.job_controller.job_config import create_pod_spec
from src.logger import get_logger

logger = get_logger()

config.load_incluster_config()
v1 = client.CoreV1Api()
batch_v1 = client.BatchV1Api()


def kube_create_job_object(job_name: str, namespace: str, name, image, env_vars):
    body = client.V1Job(api_version="batch/v1", kind="Job")
    body.metadata = client.V1ObjectMeta(namespace=namespace, name=job_name)
    body.status = client.V1JobStatus()
    template = client.V1PodTemplate()
    template.template = client.V1PodTemplateSpec()
    template.template.spec = create_pod_spec(client, name, image, env_vars)
    body.spec = client.V1JobSpec(template=template.template, backoff_limit=0)
    return body


def kube_create_job(name, image, env_vars, namespace):
    # Create the job definition
    job_name = f"{name}{shortuuid.ShortUUID().random(length=8).lower()}"
    body = kube_create_job_object(
        job_name,
        namespace,
        name,
        image,
        env_vars,
    )
    try:
        api_response = batch_v1.create_namespaced_job(
                            namespace, body, pretty=True,
                            )
        logger.debug(api_response)
    except ApiException as e:
        logger.error(
            f"Exception when calling BatchV1Api->create_namespaced_job: {e}"
        )
    return


def spawn_k8s_jobs(file_names: list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        _ = {
            executor.submit(kube_create_job, file_name): file_name
            for file_name in file_names
        }
