# GlassKube


GlassKube is a simple server-client app for k8s training. It displays an inventory of the glassKube namespace in the cluster and a hierarchy graph of the entire cluster
   
Deploy the following YAMLs to your cluster:

* [glasskube-deployment.yaml](glasskube-deployment.yaml)
* [glasskube-permissions.yaml](glasskube-permissions.yaml)
* [glasskube-service.yaml](glasskube-service.yaml)

This will spinup a server based on the GlassKube image in DockerHub
The server will describe the cluster internals using a ClusterRole and will be accessible externally via a LoadBalancer service.