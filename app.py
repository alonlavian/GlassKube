from kubernetes import client, config
from flask import Flask, render_template
from graph_mermaid import generate_kubernetes_hierarchy_mermaid

# Load the Kubernetes configuration from the default location
config.load_kube_config()

# Create a Kubernetes API client
api = client.CoreV1Api()

# Create a Flask application
app = Flask(__name__)


# Define a route that displays the current state of the Kubernetes cluster
@app.route('/')
def home():
    # Retrieve information about the Pods in the cluster
    pods = api.list_pod_for_all_namespaces().items

    # Retrieve information about the Services in the cluster
    services = api.list_service_for_all_namespaces().items

    # Render a template that displays the information about the Pods and Services
    return render_template('home.html', pods=pods, services=services)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/graph/')
def graph_mermaid():
    graph = generate_kubernetes_hierarchy_mermaid()
    return render_template('graph_m.html', diagramString=graph)


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
