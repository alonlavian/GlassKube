from kubernetes import client, config
import json


def get_nodes():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    nodes = v1.list_node().items
    return nodes


def get_pods():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces().items
    return pods


def get_services():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces().items
    return services


def build_json_data():
    nodes = get_nodes()
    pods = get_pods()
    services = get_services()

    nodes_data = []
    for node in nodes:
        nodes_data.append({'name': node.metadata.name})

    pods_data = []
    for pod in pods:
        pods_data.append({'name': pod.metadata.name, 'node': pod.spec.node_name})

    services_data = []
    for service in services:
        if service.spec.type == 'ClusterIP':
            services_data.append(
                {'name': service.metadata.name, 'type': 'ClusterIP', 'selector': service.spec.selector})
        elif service.spec.type == 'NodePort':
            services_data.append(
                {'name': service.metadata.name, 'type': 'NodePort', 'port': service.spec.ports[0].node_port,
                 'selector': service.spec.selector})
        elif service.spec.type == 'LoadBalancer':
            services_data.append(
                {'name': service.metadata.name, 'type': 'LoadBalancer', 'ip': service.spec.load_balancer_ingress[0].ip,
                 'selector': service.spec.selector})

    data = {'nodes': nodes_data, 'pods': pods_data, 'services': services_data}
    return json.dumps(data)


# Another implementation option
config.load_kube_config()
api_instance = client.AppsV1Api()

def get_deployments():
    deployments = api_instance.list_deployment_for_all_namespaces()
    deployment_hierarchy = []
    for deployment in deployments.items:
        deployment_dict = {'name': deployment.metadata.name, 'replicas': deployment.spec.replicas}
        pods = api_instance.list_namespaced_pod(deployment.metadata.namespace,
                                                label_selector=f'app={deployment.metadata.name}').items
        pod_hierarchy = []
        for pod in pods:
            container_hierarchy = []
            for container in pod.spec.containers:
                container_hierarchy.append(container.name)
            pod_hierarchy.append({'name': pod.metadata.name, 'containers': container_hierarchy})
        deployment_dict['pods'] = pod_hierarchy
        deployment_hierarchy.append(deployment_dict)
    return jsonify(deployment_hierarchy)
