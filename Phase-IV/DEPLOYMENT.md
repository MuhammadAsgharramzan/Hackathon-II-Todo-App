# Phase IV Deployment Guide

## Overview
This directory contains the AI-generated artifacts for deploying the Todo App to a local Kubernetes cluster (Minikube).
Due to the absence of `docker`, `minikube`, and `helm` in the current environment, the deployment steps must be executed manually.

## Artifacts Generated
1.  **Dockerfiles**:
    - Backend: `Phase-II/backend/Dockerfile`
    - Frontend: `Phase-II/frontend/Dockerfile`
2.  **Kubernetes Manifests** (Raw YAML):
    - Location: `Phase-IV/k8s/`
3.  **Helm Chart**:
    - Location: `Phase-IV/charts/todo-app/`

## Deployment Steps

### 1. Build Docker Images
Navigate to the project root and run:
```bash
# Backend
docker build -t todo-backend:latest ./Phase-II/backend

# Frontend
docker build -t todo-frontend:latest ./Phase-II/frontend
```

### 2. Load Images into Minikube
```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
# Or for older minikube:
# eval $(minikube docker-env)
# Re-run docker build commands
```

### 3. Deploy via Helm
```bash
cd Phase-IV
helm install todo-app ./charts/todo-app
```

### 4. Verify Deployment
```bash
kubectl get pods
# Wait for status 'Running'
minikube service todo-app-frontend --url
```

## Success Confirmation
Once deployed, accessing the URL provided by `minikube service` should show the Todo App UI. Creating a task via the Chatbot interface should trigger the backend and persist data to the Postgres database running in the cluster.
