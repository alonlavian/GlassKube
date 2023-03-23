from kubernetes import client, config


def generate_kubernetes_hierarchy_mermaid():
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API clients
    api = client.AppsV1Api()
    core_api = client.CoreV1Api()

    # Get the list of namespaces
    namespaces = core_api.list_namespace().items

    # Define the Mermaid code for the chart
    chart_definition = """
    graph TD;
        cluster_cluster1((Cluster))
    """

    for ns in namespaces:
        namespace = ns.metadata.name
        chart_definition += f"    namespace_{namespace}({namespace}) \n"
        chart_definition += f"    cluster_cluster1 --> namespace_{namespace} \n"

        # Get a list of all deployments in the namespace
        deployments = api.list_namespaced_deployment(namespace=namespace).items
        for deployment in deployments:
            deployment_name = deployment.metadata.name
            chart_definition += f"    deployment_{namespace}_{deployment_name}({deployment_name}) \n"
            chart_definition += f"    namespace_{namespace} --> deployment_{namespace}_{deployment_name} \n"

            replicasets = api.list_namespaced_replica_set(namespace=namespace, label_selector=f'app={deployment_name}').items
            for replicaset in replicasets:
                replicaset_name = replicaset.metadata.name
                chart_definition += f"    replica_set_{deployment_name}_{replicaset_name}({replicaset_name}) \n"
                chart_definition += f"    deployment_{namespace}_{deployment_name} --> replica_set_{deployment_name}_{replicaset_name} \n"

                pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=f'app={deployment_name}').items
                for pod in pods:
                    pod_name = pod.metadata.name
                    chart_definition += f"    pod_{replicaset_name}_{pod_name}({pod_name}) \n"
                    chart_definition += f"    replica_set_{deployment_name}_{replicaset_name} --> pod_{replicaset_name}_{pod_name} \n"

    print(chart_definition)

    return chart_definition


if __name__ == '__main__':
    generate_kubernetes_hierarchy_mermaid()
