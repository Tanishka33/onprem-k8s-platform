# Architecture Flow Explanation

The platform is built using a kubeadm-based Kubernetes cluster consisting of one control plane node and two worker nodes.

The control plane manages the overall cluster using core Kubernetes components such as the API server, scheduler, controller manager, and etcd.

The application is divided into two workload categories:

* **Shared Applications**
* **Critical Applications**

Shared applications include the frontend and backend services, which run on the shared worker node. Critical workloads such as MySQL run only on the critical worker node using node affinity, taints, and tolerations for controlled placement.

An internet user accesses the application through the NGINX Ingress Controller exposed using NodePort. The ingress controller routes:

* `/` requests to the frontend service
* `/api/*` requests to the backend service

Frontend and backend communicate internally using Kubernetes ClusterIP services and CoreDNS-based service discovery.

The backend communicates securely with the MySQL database using the internal DNS name:

`mysql-service.critical-apps.svc.cluster.local`


MySQL data is stored persistently using PersistentVolume and PersistentVolumeClaim so that data remains available even after pod restarts.

Runtime reliability is implemented using Kubernetes startup, readiness, and liveness probes to ensure applications start correctly, become available only when ready, and recover automatically from failures.

Calico CNI provides pod networking across nodes, while VXLAN encapsulation enables reliable cross-node communication in the AWS-hosted on-prem environment.

ResourceQuota and LimitRange are used to enforce workload governance and resource control inside namespaces.
