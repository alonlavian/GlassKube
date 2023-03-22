import graphviz
from kubernetes import client, config

def generate_kubernetes_hierarchy(namespace=None):
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api = client.AppsV1Api()
    core_api =  client.CoreV1Api()

    # Get the list of namespaces
    namespaces =  core_api.list_namespace()
    # Get the list of deployments
    # deployments = api.list_deployment_for_all_namespaces().items

    # Create a Graphviz graph
    graph = graphviz.Digraph()

    # Add nodes for the clusters and namespaces
    graph.node('cluster', label='Kubernetes Cluster')
    # graph.node('namespace', label='Namespace')

    # Add edges to connect the nodes
    # graph.edge('cluster', 'namespace')

    # if namespace:
    #     graph.node(namespace, label=namespace)
    #     graph.edge('cluster', namespace)

    for ns in namespaces.items:
        namespace = ns.metadata.name
        graph.node(namespace, label=namespace)
        graph.edge('cluster', namespace)
    # Add nodes for the deployments, replicasets, and pods
        deployments = api.list_namespaced_deployment(namespace=namespace).items
        for deployment in deployments:
            deployment_name = deployment.metadata.name
            graph.node(deployment_name, label=deployment_name)
            graph.edge(namespace, deployment_name)

            replicasets = api.list_namespaced_replica_set(namespace=namespace, label_selector=f'app={deployment_name}').items

            for replicaset in replicasets:
                replicaset_name = replicaset.metadata.name
                graph.node(replicaset_name, label=replicaset_name)
                graph.edge(deployment_name, replicaset_name)

                pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=f'app={deployment_name}').items

                for pod in pods:
                    pod_name = pod.metadata.name
                    graph.node(pod_name, label=pod_name)
                    graph.edge(replicaset_name, pod_name)

    # Render the graph
    graph.format = "svg"
    return graph.render('kubernetes_hierarchy', view=True)

if __name__ == '__main__':
    generate_kubernetes_hierarchy()