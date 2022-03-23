from src.job_controller.utils import create_container


def create_pod_spec(client, name, image, env_vars):
    toleration = client.V1Toleration(
        key="reserved-pool",
        operator="Equal",
        value="true",
        effect="NoSchedule",
    )
    container = create_container(
        client,
        name=name,
        image=image,
        image_pull_policy="Always",
        env_vars=env_vars,
        resource_requirements={"cpu": "200m"},
    )
    return client.V1PodSpec(
        containers=[container],
        restart_policy="OnFailure",
        tolerations=[toleration],
    )
