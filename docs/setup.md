# TLS Setup

Generate certificate:

openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout tls.key \
-out tls.crt \
-subj "/CN=feedback.local/O=feedback"

Create secret:

kubectl create secret tls feedback-tls \
--cert=tls.crt \
--key=tls.key \
-n shared-apps

# Setup Order

1. Create namespaces

kubectl apply -f namespaces/

2. Create secrets

kubectl apply -f storage/mysql-secret.yaml

3. Create storage

kubectl apply -f storage/

4. Deploy MySQL

kubectl apply -f storage/mysql-statefulset.yaml

5. Deploy applications

kubectl apply -f deployments/

6. Install ingress controller

7. Create TLS secret

kubectl create secret tls ...

8. Apply ingress

kubectl apply -f ingress/