import os
from kubernetes import client


token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
with open(token_path) as f:
    token = f.read()

print(token)
# Configure the Kubernetes API client with the Service Account token
configuration = client.Configuration()
configuration.host = f"https://{os.environ['KUBERNETES_SERVICE_HOST']}:{os.environ['KUBERNETES_SERVICE_PORT']}"
configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
configuration.verify_ssl = False
configuration.debug = False
configuration.assert_hostname = True
configuration.api_key = {'authorization': f'Bearer {token}'}

# Create a Kubernetes API client
api_client = client.ApiClient(configuration=configuration)

# Create a Kubernetes API clients
core_api = client.CoreV1Api(api_client)
api = client.AppsV1Api(api_client)


def generate_kubernetes_hierarchy_mermaid():


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

def list_kubernetes_objects():
    # Retrieve information about the Pods in the cluster
    pods = core_api.list_namespaced_pod(namespace='default').items

    # Retrieve information about the Services in the cluster
    services = core_api.list_namespaced_service(namespace='default').items

    return pods, services

if __name__ == '__main__':
    generate_kubernetes_hierarchy_mermaid()
