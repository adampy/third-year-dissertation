# Obtained from https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises

# Install Calico operator and custom resource definitions
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.2/manifests/tigera-operator.yaml

# Install necessary custom resource
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.2/manifests/custom-resources.yaml
