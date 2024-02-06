kubectl apply -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/v1.4.0/cluster.yaml
kubectl apply -f deployment.yaml
docker build -t python-custom-autoscaler .
kubectl apply -f cpa.yaml

# Optionally expose the service
kubectl expose deployment/hello-kubernetes --type="NodePort" --name=python-custom-autoscaler --port 8080 --target-port 8080