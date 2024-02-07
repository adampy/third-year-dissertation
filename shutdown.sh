# Shutdown CPA and the application
kubectl delete -f cpa.yaml
kubectl delete -f deployment.yaml

# Shutdown CPA lib
kubectl delete -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/v1.4.0/cluster.yaml

# Shutdown Metrics API
cd metrics-server
./delete.sh
cd ..

# Shutdown exposed service if it was created
kubectl delete service hello-kubernetes