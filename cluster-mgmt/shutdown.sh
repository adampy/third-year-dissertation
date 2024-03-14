# Shutdown CPA and the application
kubectl delete cpa --all

# Shutdown CPA lib
kubectl delete -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/v1.4.0/cluster.yaml

# Shutdown Metrics API
kubectl delete -f ./metrics-server.yaml

# Shutdown exposed service if it was created
kubectl delete pods,deployments,services -l app=teastore