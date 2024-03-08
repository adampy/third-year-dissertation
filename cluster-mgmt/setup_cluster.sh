sudo kubeadm init --cri-socket unix:///var/run/cri-dockerd.sock --pod-network-cidr=10.0.128.0/17

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
