# Phase IV Deployment Guide

## Overview

This guide provides multiple deployment options for the Todo App Phase IV Kubernetes deployment. Choose the option that best fits your environment.

## Prerequisites

All options require:
- Docker images built: `todo-backend:latest` and `todo-frontend:latest`
- Docker installed and running

## Deployment Options

### Option 1: Kind (Kubernetes in Docker) - Recommended for WSL2/Linux

**Best for**: Local development, WSL2 environments, CI/CD testing

**Advantages**:
- Works in WSL2 without driver issues
- Fast cluster creation
- Full Kubernetes feature support
- Easy cleanup

**Steps**:

```bash
# Run the automated deployment script
cd Phase-IV
./scripts/deploy-kind.sh
```

**Manual steps** (if you prefer):

```bash
# 1. Install kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# 2. Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 3. Create cluster
kind create cluster --name todo-app

# 4. Load images
kind load docker-image todo-backend:latest --name todo-app
kind load docker-image todo-frontend:latest --name todo-app

# 5. Deploy
helm install todo-app ./charts/todo-app

# 6. Port forward to access
kubectl port-forward svc/todo-frontend 3000:3000
kubectl port-forward svc/todo-backend 8000:8000
```

**Access**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

**Cleanup**:
```bash
kind delete cluster --name todo-app
```

---

### Option 2: Docker Compose - Simplest for Local Testing

**Best for**: Quick local testing without Kubernetes

**Advantages**:
- No Kubernetes required
- Fastest startup
- Simple configuration
- Easy debugging

**Steps**:

```bash
cd Phase-IV
docker-compose up -d
```

**Access**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432

**View logs**:
```bash
docker-compose logs -f
```

**Cleanup**:
```bash
docker-compose down -v
```

---

### Option 3: Minikube - Traditional Approach

**Best for**: Environments with proper virtualization support

**Requirements**:
- VirtualBox, KVM2, or Hyper-V installed
- Not recommended for WSL2

**Steps**:

```bash
# 1. Start Minikube
minikube start --memory=4096 --cpus=2

# 2. Load images
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# 3. Install Helm (if not installed)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 4. Deploy
helm install todo-app ./charts/todo-app

# 5. Access services
minikube service todo-frontend --url
```

---

### Option 4: Cloud Kubernetes (GKE/EKS/AKS) - Production

**Best for**: Production deployments, team collaboration

**Prerequisites**:
- Cloud account (GCP/AWS/Azure)
- Container registry (GCR/ECR/ACR)
- kubectl configured for your cluster

**Steps**:

```bash
# 1. Tag and push images to registry
docker tag todo-backend:latest <registry>/todo-backend:latest
docker tag todo-frontend:latest <registry>/todo-frontend:latest
docker push <registry>/todo-backend:latest
docker push <registry>/todo-frontend:latest

# 2. Update Helm values
cat > custom-values.yaml <<EOF
backend:
  image:
    repository: <registry>/todo-backend
    tag: latest
frontend:
  image:
    repository: <registry>/todo-frontend
    tag: latest
EOF

# 3. Deploy to cloud cluster
kubectl config use-context <your-cluster>
helm install todo-app ./charts/todo-app -f custom-values.yaml

# 4. Get external IP
kubectl get services
```

---

## Verification Steps

After deployment with any option:

### 1. Check Pod Status
```bash
kubectl get pods
# All pods should show STATUS: Running
```

### 2. Check Services
```bash
kubectl get services
```

### 3. Test Health Endpoints
```bash
# Backend health
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Backend readiness
curl http://localhost:8000/ready
# Should return: {"status":"ready","database":"connected"}

# Frontend health
curl http://localhost:3000/api/health
# Should return: {"status":"healthy",...}
```

### 4. Test Application
- Open browser to http://localhost:3000
- Register a new user
- Create a task via chatbot
- Verify task appears in list

---

## Troubleshooting

### Pods Not Starting

```bash
# Check pod logs
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend

# Check pod events
kubectl describe pod <pod-name>
```

### Database Connection Issues

```bash
# Check postgres pod
kubectl logs -l app=postgres

# Verify secrets
kubectl get secret todo-secrets -o yaml
```

### Image Pull Errors

```bash
# For kind: Reload images
kind load docker-image todo-backend:latest --name todo-app

# For Minikube: Reload images
minikube image load todo-backend:latest
```

### Port Already in Use

```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process or use different ports
kubectl port-forward svc/todo-frontend 3001:3000
```

---

## Performance Testing

After deployment, run performance tests:

```bash
# Install k6 (load testing tool)
sudo apt-get install k6

# Run load test
k6 run - <<EOF
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 100,
  duration: '30s',
};

export default function() {
  let res = http.get('http://localhost:8000/health');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
EOF
```

---

## Security Checklist

Before production deployment:

- [ ] Update secrets in `k8s/secrets.yaml` or Helm values
- [ ] Rotate JWT secret key
- [ ] Secure Gemini API key
- [ ] Run vulnerability scan: `./scripts/scan-containers.sh`
- [ ] Enable network policies
- [ ] Configure RBAC
- [ ] Set up TLS/SSL certificates
- [ ] Enable pod security policies

---

## Monitoring Setup

### Deploy Prometheus & Grafana

```bash
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus stack
helm install prometheus prometheus-community/kube-prometheus-stack

# Access Grafana
kubectl port-forward svc/prometheus-grafana 3001:80
# Default credentials: admin/prom-operator
```

### View Metrics

Backend and frontend expose `/metrics` endpoints (configured in Task 4.4).

---

## Next Steps

1. Choose your deployment option
2. Run the deployment
3. Verify all services are healthy
4. Run integration tests (Phase 6)
5. Set up monitoring
6. Configure CI/CD pipeline

---

## Support

For issues:
1. Check logs: `kubectl logs <pod-name>`
2. Review events: `kubectl get events`
3. Consult `IMPLEMENTATION_STATUS.md` for detailed status
4. Check health endpoints for service status
