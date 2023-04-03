from flask import Flask, render_template
from k8s import generate_kubernetes_hierarchy_mermaid, list_kubernetes_objects

# Create a Flask application
app = Flask(__name__)


# Define a route that displays the current state of the Kubernetes cluster
@app.route('/')
def home():

   pods, services = list_kubernetes_objects()
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
    app.run(host='0.0.0.0', port=5000, debug=True)
