kubectl delete -f cpa.yaml
kubectl delete -f deployment.yaml
kubectl delete -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/v1.4.0/cluster.yaml
kubectl delete service hello-kubernetes