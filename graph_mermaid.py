from kubernetes import client, config
# import markdown

def generate_kubernetes_hierarchy_mermaid():

    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api = client.AppsV1Api()
    core_api = client.CoreV1Api()

    # Get the list of namespaces
    namespaces = core_api.list_namespace().items
    # Get a list of all namespaces
    # namespaces = api.list_namespace().items

    # Create a new Mermaid chart
    # chart = ui.mermaid

    # Define the Mermaid code for the chart
    chart_definition = """
    graph TD;
        cluster_cluster1[Cluster]
    """

    for namespace in namespaces:
        namespace_name = namespace.metadata.name
        chart_definition += f"    namespace_{namespace_name}[{namespace_name}] \n"
        chart_definition += f"    cluster_cluster1 --> namespace_{namespace_name} \n"

        # Get a list of all deployments in the namespace
        deployments = api.list_namespaced_deployment(namespace=namespace_name).items

        for deployment in deployments:
            deployment_name = deployment.metadata.name
            chart_definition += f"    deployment_{namespace_name}_{deployment_name}[{deployment_name}] \n"
            chart_definition += f"    replica_set_{namespace_name}_{deployment_name}[ReplicaSet] \n"
            chart_definition += f"    pod_{namespace_name}_{deployment_name}[Pod] \n"
            chart_definition += f"    namespace_{namespace_name} --> deployment_{namespace_name}_{deployment_name} \n"
            chart_definition += f"    deployment_{namespace_name}_{deployment_name} --> replica_set_{namespace_name}_{deployment_name} \n"
            chart_definition += f"    replica_set_{namespace_name}_{deployment_name} --> pod_{namespace_name}_{deployment_name} \n"

    # Set the chart definition
    # chart.set_definition(chart_definition)

    # Render the chart
    print(chart_definition)
    # html = markdown.markdown(chart_definition, extensions=['md_mermaid'])
    return chart_definition


if __name__ == '__main__':
    generate_kubernetes_hierarchy_mermaid()
