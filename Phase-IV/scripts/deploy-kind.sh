#!/bin/bash
# Kind (Kubernetes in Docker) Deployment Script
# Alternative to Minikube for WSL2/Linux environments

set -e

echo "=== Todo App - Kind Deployment Script ==="
echo ""

# Check if kind is installed
if ! command -v kind &> /dev/null; then
    echo "Installing kind..."
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
    echo "✓ Kind installed"
else
    echo "✓ Kind already installed"
fi

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "Installing Helm..."
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    echo "✓ Helm installed"
else
    echo "✓ Helm already installed"
fi

echo ""
echo "Creating kind cluster..."
kind create cluster --name todo-app --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000
    hostPort: 3000
    protocol: TCP
  - containerPort: 30001
    hostPort: 8000
    protocol: TCP
EOF

echo "✓ Kind cluster created"
echo ""

# Load Docker images into kind
echo "Loading Docker images into kind cluster..."
kind load docker-image todo-backend:latest --name todo-app
kind load docker-image todo-frontend:latest --name todo-app
echo "✓ Images loaded"
echo ""

# Deploy with Helm
echo "Deploying Todo App with Helm..."
cd "$(dirname "$0")/.."
helm install todo-app ./charts/todo-app \
  --set frontend.service.type=NodePort \
  --set frontend.service.nodePort=30000 \
  --set backend.service.type=NodePort \
  --set backend.service.nodePort=30001

echo "✓ Deployment complete"
echo ""

# Wait for pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=120s
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s

echo ""
echo "=== Deployment Status ==="
kubectl get pods
echo ""
kubectl get services
echo ""

echo "=== Access Information ==="
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo ""
echo "To view logs:"
echo "  kubectl logs -l app=todo-backend"
echo "  kubectl logs -l app=todo-frontend"
echo ""
echo "To delete the cluster:"
echo "  kind delete cluster --name todo-app"
