Installed:
- containerd
- kubeadm
- kubelet
- kubectl
- Calico CNI
- NGINX Ingress Controller

Cluster:
- 1 Control Plane
- 2 Worker Nodes

Node Labels:
- workload=shared
- workload=critical

Node Taints:
- critical=true:NoSchedule