def create_secret(client, key, name):
    secret_key = client.V1SecretKeySelector(key=key, name=name)
    return client.V1EnvVar(
        value_from=client.V1EnvVarSource(
            secret_key_ref=secret_key),
        name=key,
    )


def create_configmap(client, key, name):
    configmap_var = client.V1ConfigMapKeySelector(
            key=key, name=name
        )
    return client.V1EnvVar(
        name=key, value_from=client.V1EnvVarSource(
            config_map_key_ref=configmap_var
        )
    )


def create_env_list(client, env_vars) -> list:
    return [
        client.V1EnvVar(name=env_name, value=env_value)
        for env_name, env_value in env_vars.items()
    ]


def create_container(
    client,
    name,
    image,
    image_pull_policy,
    env_vars,
    resource_requirements: dict,
):
    resources = client.V1ResourceRequirements(
                requests=resource_requirements
            )
    env_list = create_env_list(client, env_vars)
    return client.V1Container(
                name=name,
                image=image,
                env=env_list,
                image_pull_policy=image_pull_policy,
                resources=resources,
            )
