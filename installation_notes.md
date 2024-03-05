# Running `docker` as non-sudo (i.e. adding current user to docker group)
https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

# Installing cri-dockerd
https://www.mirantis.com/blog/how-to-install-cri-dockerd-and-migrate-nodes-from-dockershim/

# For initialising a K8 cluster (using kubeadm) - RUN THIS EVERYTIME WE BOOT UP MASTER (added into `~/.bashrc`)
```bash
sudo kubeadm init --cri-socket unix:///var/run/cri-dockerd.sock
```

Followed by...

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

# Getting K8 working (to prevent "API timeout" errors)
```bash
KUBECONFIG=$HOME/.kube/config
```

# Installing Calico
https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises

# For adding a secret (allowing pulling from privare docker-hub repository)
https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line
```bash
kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v2/ --docker-username=adamc1234 --docker-password="jMt+nE8&exXYqGj" --docker-email=adamflint8@hotmail.co.uk
```

# Get join command (for adding worker nodes)
```bash
kubeadm token create --print-join-command
```

# Joining as worker node
```bash
sudo kubeadm join 10.0.0.4:6443 --token 55edt2.lk984h2rf9z11naa --discovery-token-ca-cert-hash sha256:25310b5c17508210ad674808a23f26c907114b6fc966f06b20837c0f7fbaed8f --cri-socket unix:///var/run/cri-dockerd.sock
```

# If DNS names cannot be resolved inside the pods after installation and deployment
https://stackoverflow.com/questions/45805483/kubernetes-pods-cant-resolve-hostnames
```bash
kubectl -n kube-system rollout restart deployment coredns
```

# For installing Prometheus using Helm
https://helm.sh/docs/intro/install/#from-script
https://github.com/prometheus-community/helm-charts / https://www.youtube.com/watch?v=Nng7z7xGh7g
