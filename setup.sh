# Install Metrics API
cd metrics-server
./apply.sh
cd ..

# Install CPA
kubectl apply -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/v1.4.0/cluster.yaml

# Install the application
kubectl apply -f deployment.yaml

# Build and apply custom autoscaler
docker build -t python-custom-autoscaler .
kubectl apply -f cpa.yaml

# Optionally expose the service
kubectl expose deployment/hello-kubernetes --type="NodePort" --name=python-custom-autoscaler --port 8080 --target-port 8080